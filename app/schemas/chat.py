from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid


class ChatMessageCreate(BaseModel):
    content: str
    conversation_id: Optional[uuid.UUID] = None
    session_type: str = "free_talk"


class ChatMessageResponse(BaseModel):
    message_id: uuid.UUID
    response: str
    crisis_detected: bool
    crisis_resources: Optional[Dict] = None
    tokens_used: Optional[int] = None


class ConversationResponse(BaseModel):
    id: uuid.UUID
    session_type: str
    started_at: datetime
    message_count: int
    
    class Config:
        from_attributes = True
