from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import security_manager
from app.services.user_service import UserService
from app.models.user import User
import uuid


async def get_current_user(
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
) -> User:
    user_service = UserService(db)
    user = await user_service.get_user_by_id(uuid.UUID(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_premium_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    
    return current_user
