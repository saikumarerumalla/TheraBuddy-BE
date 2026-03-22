from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import security_manager
from app.utils.encryption import encryption_manager
import uuid
from datetime import datetime


class UserService:
    """Handle user operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        is_anonymous: bool = False,
        onboarding_data: Optional[Dict] = None
    ) -> User:
        """Create a new user"""
        
        user = User(
            email=email,
            hashed_password=security_manager.hash_password(password) if password else None,
            is_anonymous=is_anonymous
        )
        
        # Add onboarding data if provided
        if onboarding_data:
            user.age_range = onboarding_data.get("age_range")
            user.gender = onboarding_data.get("gender")
            user.prefecture = onboarding_data.get("prefecture")
            user.language_preference = onboarding_data.get("language_preference", "en")
            
            # Encrypt sensitive data
            if onboarding_data.get("has_previous_therapy"):
                user.has_previous_therapy = encryption_manager.encrypt(
                    str(onboarding_data["has_previous_therapy"])
                )
            
            if onboarding_data.get("current_medication"):
                user.current_medication = encryption_manager.encrypt(
                    str(onboarding_data["current_medication"])
                )
            
            user.primary_concerns = onboarding_data.get("primary_concerns")
            user.well_being_score = onboarding_data.get("well_being_score")
            user.concern_duration = onboarding_data.get("concern_duration")
            user.life_situation = onboarding_data.get("life_situation")
            user.living_situation = onboarding_data.get("living_situation")
            user.support_system = onboarding_data.get("support_system")
            user.therapy_goals = onboarding_data.get("therapy_goals")
            user.conversation_style = onboarding_data.get("conversation_style", "balanced")
            user.ai_companion_style = onboarding_data.get("ai_companion_style", "professional_assistant")
            user.notification_preferences = onboarding_data.get("notification_preferences")
            user.checkin_frequency = onboarding_data.get("checkin_frequency", "daily")
            
            user.onboarding_completed = True
            user.data_consent = onboarding_data.get("data_consent", False)
            user.terms_accepted = onboarding_data.get("terms_accepted", False)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        
        user = await self.get_user_by_email(email)
        
        if not user:
            return None
        
        if not user.hashed_password:
            return None
        
        if not security_manager.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def update_user_profile(
        self,
        user_id: uuid.UUID,
        update_data: Dict
    ) -> User:
        """Update user profile"""
        
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise ValueError("User not found")
        
        # Update allowed fields
        allowed_fields = [
            "age_range", "gender", "prefecture", "language_preference",
            "primary_concerns", "therapy_goals", "conversation_style",
            "ai_companion_style", "notification_preferences", "checkin_frequency"
        ]
        
        for field in allowed_fields:
            if field in update_data:
                setattr(user, field, update_data[field])
        
        user.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def update_crisis_risk(
        self,
        user_id: uuid.UUID,
        risk_level: str
    ):
        """Update user's crisis risk level"""
        
        user = await self.get_user_by_id(user_id)
        
        if user:
            user.crisis_risk_level = risk_level
            user.last_crisis_check = datetime.utcnow()
            await self.db.commit()
    
    async def delete_user(self, user_id: uuid.UUID):
        """Delete user and all associated data"""
        
        user = await self.get_user_by_id(user_id)
        
        if user:
            await self.db.delete(user)
            await self.db.commit()
