from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserResponse
from app.models.user import User
from typing import Dict

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return UserResponse.from_orm(current_user)


@router.put("/me")
async def update_current_user(
    update_data: Dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    
    updated_user = await user_service.update_user_profile(
        user_id=current_user.id,
        update_data=update_data
    )
    
    return UserResponse.from_orm(updated_user)


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    await user_service.delete_user(current_user.id)
    
    return {"message": "User account deleted successfully"}
