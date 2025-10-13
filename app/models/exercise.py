"""Exercise and activity tracking"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class ExerciseCompletion(Base):
    """Track completed exercises"""
    __tablename__ = "exercise_completions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    exercise_id = Column(String, nullable=False)  # Reference to exercise catalog
    exercise_type = Column(String, nullable=False)  # breathing, cbt, mindfulness, etc.
    exercise_name = Column(String, nullable=False)
    
    duration_seconds = Column(Integer, nullable=True)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # User Feedback
    helpful_rating = Column(Integer, nullable=True)  # 1-5
    difficulty_rating = Column(Integer, nullable=True)  # 1-5
    notes = Column(String, nullable=True)
    
    # Context
    mood_before = Column(Integer, nullable=True)
    mood_after = Column(Integer, nullable=True)


class Goal(Base):
    """User goals and progress"""
    __tablename__ = "goals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    goal_text = Column(String, nullable=False)
    goal_category = Column(String, nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)
    
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    progress_percentage = Column(Integer, default=0)
    milestones = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
