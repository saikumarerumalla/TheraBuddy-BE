from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import security_manager
from app.services.user_service import UserService
from app.schemas.user import UserCreate, TokenResponse, OnboardingData
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    onboarding: OnboardingData,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    
    user_service = UserService(db)
    
    # Check if email already exists
    if user_data.email:
        existing_user = await user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create user
    user = await user_service.create_user(
        email=user_data.email,
        password=user_data.password,
        is_anonymous=user_data.is_anonymous,
        onboarding_data=onboarding.dict()
    )
    
    # Create tokens
    access_token = security_manager.create_access_token(
        data={"sub": str(user.id)}
    )
    refresh_token = security_manager.create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """Login user"""
    
    user_service = UserService(db)
    user = await user_service.authenticate_user(email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = security_manager.create_access_token(
        data={"sub": str(user.id)}
    )
    refresh_token = security_manager.create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
