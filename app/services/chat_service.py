"""Chat service for managing conversations"""

from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.conversation import Conversation, Message
from app.models.crisis import CrisisEvent
from app.services.llm.base import LLMMessage
from app.services.llm.openai_service import OpenAIService
from app.services.llm.anthropic_service import AnthropicService
from app.services.llm.prompt_manager import PromptManager
from app.services.llm.safety_filter import SafetyFilter
from app.utils.encryption import encryption_manager
from app.config import get_settings
import uuid

settings = get_settings()


class ChatService:
    """Handle chat conversations and LLM interactions"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
        # Initialize LLM service based on config
        if settings.LLM_PROVIDER == "openai":
            self.llm_service = OpenAIService()
        else:
            self.llm_service = AnthropicService()
    
    async def create_conversation(
        self,
        user_id: uuid.UUID,
        session_type: str = "free_talk"
    ) -> Conversation:
        """Create a new conversation session"""
        
        conversation = Conversation(
            user_id=user_id,
            session_type=session_type
        )
        
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        
        return conversation
    
    async def get_conversation_history(
        self,
        conversation_id: uuid.UUID,
        limit: int = 50
    ) -> List[Message]:
        """Get conversation message history"""
        
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        messages = result.scalars().all()
        
        return list(reversed(messages))
    
    async def send_message(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        content: str,
        user_profile: Dict,
        stream: bool = False
    ) -> Dict:
        """
        Process user message and generate AI response
        
        Returns:
            {
                "message_id": UUID,
                "response": str,
                "crisis_detected": bool,
                "crisis_resources": Optional[Dict]
            }
        """
        
        # Detect crisis
        is_crisis, risk_level, crisis_keywords = SafetyFilter.detect_crisis(content)
        
        # Assess sentiment
        sentiment_score = SafetyFilter.assess_sentiment(content)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=encryption_manager.encrypt(content),
            content_language="en",
            sentiment_score=sentiment_score,
            crisis_keywords_detected=str(crisis_keywords) if crisis_keywords else None,
            safety_flagged=is_crisis
        )
        
        self.db.add(user_message)
        await self.db.commit()
        
        # If crisis detected, log crisis event
        crisis_resources = None
        if is_crisis:
            await self._handle_crisis_event(
                user_id=user_id,
                conversation_id=conversation_id,
                risk_level=risk_level,
                keywords=crisis_keywords,
                context=content
            )
            
            # Get crisis resources
            crisis_resources = self._get_crisis_resources()
        
        # Build conversation context
        conversation_history = await self.get_conversation_history(conversation_id, limit=10)
        
        # Build LLM messages
        system_prompt = PromptManager.build_system_prompt(
            user_profile=user_profile,
            is_crisis=is_crisis
        )
        
        llm_messages = [LLMMessage(role="system", content=system_prompt)]
        
        # Add conversation history
        for msg in conversation_history[:-1]:  # Exclude the message we just added
            decrypted_content = encryption_manager.decrypt(msg.content)
            llm_messages.append(LLMMessage(role=msg.role, content=decrypted_content))
        
        # Add current user message
        llm_messages.append(LLMMessage(role="user", content=content))
        
        # Generate AI response
        if stream:
            # Return generator for streaming
            return {
                "stream": self._stream_ai_response(
                    llm_messages=llm_messages,
                    conversation_id=conversation_id,
                    user_id=user_id
                ),
                "crisis_detected": is_crisis,
                "crisis_resources": crisis_resources
            }
        else:
            # Generate complete response
            llm_response = await self.llm_service.generate_response(
                messages=llm_messages,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            # Save AI response
            ai_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="assistant",
                content=encryption_manager.encrypt(llm_response.content),
                content_language="en",
                tokens_used=llm_response.tokens_used,
                model_used=llm_response.model,
                response_time_ms=llm_response.response_time_ms
            )
            
            self.db.add(ai_message)
            await self.db.commit()
            await self.db.refresh(ai_message)
            
            # Update conversation stats
            await self._update_conversation_stats(conversation_id)
            
            return {
                "message_id": str(ai_message.id),
                "response": llm_response.content,
                "crisis_detected": is_crisis,
                "crisis_resources": crisis_resources,
                "tokens_used": llm_response.tokens_used
            }
    
    async def _stream_ai_response(
        self,
        llm_messages: List[LLMMessage],
        conversation_id: uuid.UUID,
        user_id: uuid.UUID
    ):
        """Stream AI response"""
        
        full_response = ""
        
        async for chunk in self.llm_service.stream_response(
            messages=llm_messages,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS
        ):
            full_response += chunk
            yield chunk
        
        # Save complete response
        ai_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=encryption_manager.encrypt(full_response),
            content_language="en"
        )
        
        self.db.add(ai_message)
        await self.db.commit()
        
        await self._update_conversation_stats(conversation_id)
    
    async def _handle_crisis_event(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        risk_level: str,
        keywords: List[str],
        context: str
    ):
        """Log crisis event for monitoring"""
        
        crisis_event = CrisisEvent(
            user_id=user_id,
            conversation_id=conversation_id,
            risk_level=risk_level,
            keywords_detected=keywords,
            context=encryption_manager.encrypt(context),
            resources_provided=self._get_crisis_resources(),
            human_notified=(risk_level == "critical")
        )
        
        self.db.add(crisis_event)
        await self.db.commit()
        
        # In production: Send alert to human monitors if critical
        if risk_level == "critical":
            # TODO: Implement notification system (email, SMS, dashboard alert)
            pass
    
    def _get_crisis_resources(self) -> Dict:
        """Get crisis intervention resources"""
        
        return {
            "hotlines": [
                {
                    "name": "988 Suicide & Crisis Lifeline",
                    "phone": "988",
                    "hours": "24/7",
                    "language": "English"
                },
                {
                    "name": "Crisis Text Line",
                    "phone": "Text HOME to 741741",
                    "hours": "24/7",
                    "language": "English"
                }
            ],
            "emergency": [
                {
                    "name": "Emergency Services",
                    "phone": "911"
                }
            ],
            "message": "Your life matters. If you need immediate help, please call one of the numbers above."
        }
    
    async def _update_conversation_stats(self, conversation_id: uuid.UUID):
        """Update conversation statistics"""
        
        # Count messages
        query = select(func.count(Message.id)).where(
            Message.conversation_id == conversation_id
        )
        result = await self.db.execute(query)
        message_count = result.scalar()
        
        # Get conversation
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.db.execute(query)
        conversation = result.scalar_one()
        
        conversation.message_count = message_count
        
        await self.db.commit()
    
    async def end_conversation(self, conversation_id: uuid.UUID):
        """End conversation session"""
        
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.db.execute(query)
        conversation = result.scalar_one()
        
        conversation.ended_at = datetime.utcnow()
        
        if conversation.started_at:
            duration = (conversation.ended_at - conversation.started_at).total_seconds()
            conversation.duration_seconds = int(duration)
        
        await self.db.commit()
