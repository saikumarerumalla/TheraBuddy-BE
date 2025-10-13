from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.crisis import CrisisEvent
from app.utils.encryption import encryption_manager
import uuid
from datetime import datetime


class CrisisService:
    """Basic crisis event logging and retrieval"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(
        self,
        user_id: uuid.UUID,
        conversation_id: Optional[uuid.UUID],
        risk_level: str,
        keywords: List[str],
        context: str,
        resources_provided: Optional[Dict] = None,
        human_notified: bool = False,
    ) -> CrisisEvent:
        event = CrisisEvent(
            user_id=user_id,
            conversation_id=conversation_id,
            risk_level=risk_level,
            keywords_detected=keywords,
            context=encryption_manager.encrypt(context),
            resources_provided=resources_provided,
            human_notified=human_notified,
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def resolve_event(
        self,
        event_id: uuid.UUID,
        resolution_notes: Optional[str] = None
    ) -> CrisisEvent:
        query = select(CrisisEvent).where(CrisisEvent.id == event_id)
        result = await self.db.execute(query)
        event = result.scalar_one()
        event.is_resolved = True
        event.resolution_notes = resolution_notes
        event.resolved_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def list_user_events(self, user_id: uuid.UUID) -> List[CrisisEvent]:
        query = select(CrisisEvent).where(CrisisEvent.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
