from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.mood import MoodEntry
from app.models.conversation import Conversation, Message
from app.utils.helpers import get_japan_time
import uuid


class AnalyticsService:
    """Aggregate analytics for dashboard"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard(self, user_id: uuid.UUID) -> Dict:
        now = get_japan_time()

        # Total conversations
        q_conv_count = select(func.count(Conversation.id)).where(Conversation.user_id == user_id)
        conv_count = (await self.db.execute(q_conv_count)).scalar() or 0

        # Total messages
        q_msg_count = select(func.count(Message.id)).where(Message.user_id == user_id)
        msg_count = (await self.db.execute(q_msg_count)).scalar() or 0

        # Recent mood average (last 14 days)
        q_recent_mood = (
            select(func.avg(MoodEntry.overall_mood))
            .where(MoodEntry.user_id == user_id)
            .where(MoodEntry.date >= (now - func.cast(14, type(now))).date())
        )
        # Fallback: simple overall average if dialect can't cast
        avg_mood = (await self.db.execute(q_recent_mood)).scalar()

        return {
            "conversations": conv_count,
            "messages": msg_count,
            "avg_mood_recent": float(avg_mood) if avg_mood is not None else None,
        }
