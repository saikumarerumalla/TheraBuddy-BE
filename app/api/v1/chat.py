from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import security_manager
from app.services.chat_service import ChatService
from app.services.user_service import UserService
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse, ConversationResponse
from typing import List
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    message_data: ChatMessageCreate,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Send a message and get AI response"""
    
    chat_service = ChatService(db)
    user_service = UserService(db)
    
    user = await user_service.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create conversation if needed
    conversation_id = message_data.conversation_id
    if not conversation_id:
        conversation = await chat_service.create_conversation(
            user_id=uuid.UUID(user_id),
            session_type=message_data.session_type
        )
        conversation_id = conversation.id
    
    # Build user profile for context
    user_profile = {
        "language_preference": user.language_preference,
        "primary_concerns": user.primary_concerns,
        "therapy_goals": user.therapy_goals,
        "conversation_style": user.conversation_style
    }
    
    # Send message and get response
    response = await chat_service.send_message(
        user_id=uuid.UUID(user_id),
        conversation_id=conversation_id,
        content=message_data.content,
        user_profile=user_profile,
        stream=False
    )
    
    return ChatMessageResponse(**response)


@router.post("/conversation")
async def create_conversation(
    session_type: str = "free_talk",
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation session"""
    
    chat_service = ChatService(db)
    
    conversation = await chat_service.create_conversation(
        user_id=uuid.UUID(user_id),
        session_type=session_type
    )
    
    return ConversationResponse.from_orm(conversation)


@router.post("/conversation/{conversation_id}/end")
async def end_conversation(
    conversation_id: uuid.UUID,
    user_id: str = Depends(security_manager.get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """End a conversation session"""
    
    chat_service = ChatService(db)
    await chat_service.end_conversation(conversation_id)
    
    return {"message": "Conversation ended successfully"}
