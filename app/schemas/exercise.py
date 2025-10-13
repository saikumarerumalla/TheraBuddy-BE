from pydantic import BaseModel, validator
from typing import Optional


class ExerciseComplete(BaseModel):
    exercise_id: str
    exercise_type: Optional[str] = None
    exercise_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    helpful_rating: Optional[int] = None
    difficulty_rating: Optional[int] = None
    notes: Optional[str] = None

    @validator("helpful_rating", "difficulty_rating")
    def validate_ratings(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError("Rating must be between 1 and 5")
        return v
