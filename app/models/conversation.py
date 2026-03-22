"""Conversation and message models"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Conversation(Base):
    """Conversation session model"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    session_type = Column(String, default="free_talk")  # free_talk, guided_session, quick_checkin, crisis
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    message_count = Column(Integer, default=0)
    user_sentiment_avg = Column(Float, nullable=True)  # Average sentiment score
    
    summary = Column(Text, nullable=True)  # AI-generated session summary
    tags = Column(String, nullable=True)  # Comma-separated tags
    
    crisis_detected = Column(Boolean, default=False)
    crisis_resolved = Column(Boolean, default=False)


class Message(Base):
    """Individual message model"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)  # Encrypted
    content_language = Column(String, default="en")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String, nullable=True)
    
    # Sentiment & Safety
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    crisis_keywords_detected = Column(String, nullable=True)  # JSON array
    safety_flagged = Column(Boolean, default=False)
    
    # Response Quality
    response_time_ms = Column(Integer, nullable=True)
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
