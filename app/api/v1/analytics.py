from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.services.mood_service import MoodService
from app.models.user import User
from typing import Dict
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    mood_service = MoodService(db)
    
    mood_analytics = await mood_service.get_mood_analytics(
        user_id=current_user.id,
        days=30
    )
    
    return {
        "mood_analytics": mood_analytics,
        "user_since_days": (datetime.utcnow() - current_user.created_at).days if current_user.created_at else None,
        "onboarding_completed": current_user.onboarding_completed,
        "is_premium": current_user.is_premium
    }
