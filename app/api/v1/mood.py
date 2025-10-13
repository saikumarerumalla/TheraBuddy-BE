from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import security_manager
from app.services.mood_service import MoodService
from app.schemas.mood import (
    MoodEntryCreate, MoodEntryResponse,
    AssessmentCreate, AssessmentResponse
)
from typing import List
import uuid

router = APIRouter(prefix="/mood", tags=["mood"])


@router.post("/entry", response_model=MoodEntryResponse)
async def create_mood_entry(
    entry_data: MoodEntryCreate,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a mood check-in entry"""
    
    mood_service = MoodService(db)
    
    entry = await mood_service.create_mood_entry(
        user_id=uuid.UUID(user_id),
        **entry_data.dict()
    )
    
    return MoodEntryResponse.from_orm(entry)


@router.get("/history", response_model=List[MoodEntryResponse])
async def get_mood_history(
    days: int = 30,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get mood history"""
    
    mood_service = MoodService(db)
    
    history = await mood_service.get_mood_history(
        user_id=uuid.UUID(user_id),
        days=days
    )
    
    return [MoodEntryResponse.from_orm(entry) for entry in history]


@router.get("/analytics")
async def get_mood_analytics(
    days: int = 30,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get mood analytics and insights"""
    
    mood_service = MoodService(db)
    
    analytics = await mood_service.get_mood_analytics(
        user_id=uuid.UUID(user_id),
        days=days
    )
    
    return analytics


@router.post("/assessment", response_model=AssessmentResponse)
async def create_assessment(
    assessment_data: AssessmentCreate,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a standardized assessment"""
    
    mood_service = MoodService(db)
    
    # Calculate total score based on assessment type
    responses = assessment_data.responses
    total_score = sum(responses.values())
    
    assessment = await mood_service.create_assessment(
        user_id=uuid.UUID(user_id),
        assessment_type=assessment_data.assessment_type,
        responses=responses,
        total_score=total_score
    )
    
    return AssessmentResponse.from_orm(assessment)
