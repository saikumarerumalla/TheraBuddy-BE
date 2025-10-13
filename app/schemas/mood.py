from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date, datetime
import uuid


class MoodEntryCreate(BaseModel):
    overall_mood: int
    anxiety_level: Optional[int] = None
    energy_level: Optional[int] = None
    sleep_quality: Optional[int] = None
    stress_level: Optional[int] = None
    notes: Optional[str] = None
    triggers: Optional[List[str]] = None
    activities: Optional[List[str]] = None
    
    @validator("overall_mood", "anxiety_level", "energy_level", "sleep_quality", "stress_level")
    def validate_scores(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError("Score must be between 1 and 10")
        return v


class MoodEntryResponse(BaseModel):
    id: uuid.UUID
    overall_mood: int
    anxiety_level: Optional[int]
    date: date
    
    class Config:
        from_attributes = True


class AssessmentCreate(BaseModel):
    assessment_type: str
    responses: Dict
    
    @validator("assessment_type")
    def validate_type(cls, v):
        allowed = ["PHQ-9", "GAD-7", "PCL-5"]
        if v not in allowed:
            raise ValueError(f"Assessment type must be one of {allowed}")
        return v


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    assessment_type: str
    total_score: int
    severity_level: str
    completed_at: datetime
    score_change: Optional[int]
    
    class Config:
        from_attributes = True
