"""Mood tracking models"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class MoodEntry(Base):
    """Daily mood check-in"""
    __tablename__ = "mood_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Mood Dimensions (1-10 scale)
    overall_mood = Column(Integer, nullable=False)
    anxiety_level = Column(Integer, nullable=True)
    energy_level = Column(Integer, nullable=True)
    sleep_quality = Column(Integer, nullable=True)
    stress_level = Column(Integer, nullable=True)
    
    # Context
    notes = Column(String, nullable=True)  # Optional user notes (encrypted)
    triggers = Column(JSON, nullable=True)  # Identified triggers
    activities = Column(JSON, nullable=True)  # Activities that day
    
    # Timestamps
    check_in_time = Column(DateTime(timezone=True), server_default=func.now())
    date = Column(DateTime(timezone=True), nullable=False, index=True)


class Assessment(Base):
    """Standardized mental health assessments"""
    __tablename__ = "assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    assessment_type = Column(String, nullable=False)  # PHQ-9, GAD-7, PCL-5
    total_score = Column(Integer, nullable=False)
    severity_level = Column(String, nullable=True)  # minimal, mild, moderate, severe
    
    responses = Column(JSON, nullable=False)  # Individual question responses (encrypted)
    
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Comparison
    previous_score = Column(Integer, nullable=True)
    score_change = Column(Integer, nullable=True)
