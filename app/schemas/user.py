from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_anonymous: bool = False


class OnboardingData(BaseModel):
    age_range: Optional[str] = None
    gender: Optional[str] = None
    prefecture: Optional[str] = None
    language_preference: str = "ja"
    has_previous_therapy: Optional[str] = None
    current_medication: Optional[str] = None
    primary_concerns: Optional[List[str]] = None
    well_being_score: Optional[int] = None
    concern_duration: Optional[str] = None
    life_situation: Optional[List[str]] = None
    living_situation: Optional[str] = None
    support_system: Optional[List[str]] = None
    therapy_goals: Optional[List[str]] = None
    conversation_style: str = "balanced"
    ai_companion_style: str = "professional_assistant"
    notification_preferences: Optional[dict] = None
    checkin_frequency: str = "daily"
    data_consent: bool = False
    terms_accepted: bool = False
    
    @validator("well_being_score")
    def validate_well_being(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError("Well-being score must be between 1 and 10")
        return v


class UserResponse(BaseModel):
    id: uuid.UUID
    email: Optional[str]
    is_anonymous: bool
    is_premium: bool
    language_preference: str
    onboarding_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
