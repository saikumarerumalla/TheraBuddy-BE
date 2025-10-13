"""User database models"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class LanguageEnum(str, enum.Enum):
    JAPANESE = "ja"
    ENGLISH = "en"
    BOTH = "both"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    # Demographics
    age_range = Column(String, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    prefecture = Column(String, nullable=True)
    language_preference = Column(SQLEnum(LanguageEnum), default=LanguageEnum.JAPANESE)
    
    # Mental Health Background (encrypted)
    has_previous_therapy = Column(String, nullable=True)  # encrypted JSON
    current_medication = Column(String, nullable=True)  # encrypted
    
    # Current State
    primary_concerns = Column(JSON, nullable=True)  # List of concerns
    well_being_score = Column(Integer, nullable=True)  # 1-10
    concern_duration = Column(String, nullable=True)
    
    # Crisis Assessment
    crisis_risk_level = Column(String, default="low")  # low, medium, high
    last_crisis_check = Column(DateTime(timezone=True), nullable=True)
    
    # Daily Life
    life_situation = Column(JSON, nullable=True)
    living_situation = Column(String, nullable=True)
    support_system = Column(JSON, nullable=True)
    
    # Preferences
    therapy_goals = Column(JSON, nullable=True)
    conversation_style = Column(String, default="balanced")
    ai_companion_style = Column(String, default="professional_assistant")
    notification_preferences = Column(JSON, nullable=True)
    checkin_frequency = Column(String, default="daily")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_active = Column(DateTime(timezone=True), nullable=True)
    onboarding_completed = Column(Boolean, default=False)
    
    # Privacy
    data_consent = Column(Boolean, default=False)
    terms_accepted = Column(Boolean, default=False)
