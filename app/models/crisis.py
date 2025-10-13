"""Crisis event tracking and management"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class CrisisEvent(Base):
    """Track crisis events for monitoring and intervention"""
    __tablename__ = "crisis_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=True)
    
    risk_level = Column(String, nullable=False)  # low, medium, high, critical
    keywords_detected = Column(JSON, nullable=True)
    context = Column(Text, nullable=True)  # Encrypted conversation context
    
    # Response
    resources_provided = Column(JSON, nullable=True)
    human_notified = Column(Boolean, default=False)
    human_review_completed = Column(Boolean, default=False)
    
    # Resolution
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Safety Plan
    safety_plan_created = Column(Boolean, default=False)
    safety_plan_data = Column(JSON, nullable=True)  # Encrypted
    
    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Follow-up
    follow_up_scheduled = Column(Boolean, default=False)
    next_follow_up = Column(DateTime(timezone=True), nullable=True)
