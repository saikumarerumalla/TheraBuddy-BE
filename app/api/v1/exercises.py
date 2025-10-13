from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from typing import List, Dict

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/library")
async def get_exercise_library(
    category: str = None,
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    exercises = [
        {
            "id": "breathing_box",
            "name": "Box Breathing",
            "name_ja": "ボックス呼吸法",
            "category": "breathing",
            "duration_minutes": 5,
            "difficulty": "beginner",
            "description": "4-4-4-4 breathing pattern for relaxation",
            "description_ja": "リラックスのための4-4-4-4呼吸パターン"
        },
        {
            "id": "cbt_thought_record",
            "name": "Thought Record",
            "name_ja": "思考記録",
            "category": "cbt",
            "duration_minutes": 10,
            "difficulty": "intermediate",
            "description": "Identify and challenge negative thoughts",
            "description_ja": "ネガティブな思考を特定し、挑戦する"
        },
        {
            "id": "mindfulness_body_scan",
            "name": "Body Scan Meditation",
            "name_ja": "ボディスキャン瞑想",
            "category": "mindfulness",
            "duration_minutes": 15,
            "difficulty": "beginner",
            "description": "Progressive body awareness meditation",
            "description_ja": "段階的な身体意識の瞑想"
        }
    ]
    
    if category:
        exercises = [e for e in exercises if e["category"] == category]
    
    return exercises


@router.post("/complete")
async def complete_exercise(
    exercise_data: Dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # In production, save to ExerciseCompletion model
    return {"message": "Exercise completed", "data": exercise_data}
