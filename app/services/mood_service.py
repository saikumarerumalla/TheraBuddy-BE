from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from app.models.mood import MoodEntry, Assessment
from app.utils.encryption import encryption_manager
import uuid


class MoodService:
    """Handle mood tracking and analytics"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_mood_entry(
        self,
        user_id: uuid.UUID,
        overall_mood: int,
        anxiety_level: Optional[int] = None,
        energy_level: Optional[int] = None,
        sleep_quality: Optional[int] = None,
        stress_level: Optional[int] = None,
        notes: Optional[str] = None,
        triggers: Optional[List[str]] = None,
        activities: Optional[List[str]] = None
    ) -> MoodEntry:
        """Create a new mood entry"""
        
        mood_entry = MoodEntry(
            user_id=user_id,
            overall_mood=overall_mood,
            anxiety_level=anxiety_level,
            energy_level=energy_level,
            sleep_quality=sleep_quality,
            stress_level=stress_level,
            notes=encryption_manager.encrypt(notes) if notes else None,
            triggers=triggers,
            activities=activities,
            date=datetime.utcnow().date()
        )
        
        self.db.add(mood_entry)
        await self.db.commit()
        await self.db.refresh(mood_entry)
        
        return mood_entry
    
    async def get_mood_history(
        self,
        user_id: uuid.UUID,
        days: int = 30
    ) -> List[MoodEntry]:
        """Get mood history for specified days"""
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = select(MoodEntry).where(
            and_(
                MoodEntry.user_id == user_id,
                MoodEntry.date >= start_date.date()
            )
        ).order_by(MoodEntry.date.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_mood_analytics(
        self,
        user_id: uuid.UUID,
        days: int = 30
    ) -> Dict:
        """Get mood analytics and insights"""
        
        mood_history = await self.get_mood_history(user_id, days)
        
        if not mood_history:
            return {
                "average_mood": None,
                "mood_trend": "insufficient_data",
                "best_day": None,
                "worst_day": None,
                "mood_variance": None
            }
        
        # Calculate statistics
        moods = [entry.overall_mood for entry in mood_history]
        avg_mood = sum(moods) / len(moods)
        
        # Find best and worst days
        best_entry = max(mood_history, key=lambda x: x.overall_mood)
        worst_entry = min(mood_history, key=lambda x: x.overall_mood)
        
        # Calculate trend (simple linear regression)
        if len(moods) >= 7:
            recent_avg = sum(moods[:7]) / 7
            older_avg = sum(moods[-7:]) / 7
            
            if recent_avg > older_avg + 1:
                trend = "improving"
            elif recent_avg < older_avg - 1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        # Variance
        variance = sum((m - avg_mood) ** 2 for m in moods) / len(moods)
        
        return {
            "average_mood": round(avg_mood, 2),
            "mood_trend": trend,
            "best_day": {
                "date": best_entry.date.isoformat(),
                "mood": best_entry.overall_mood
            },
            "worst_day": {
                "date": worst_entry.date.isoformat(),
                "mood": worst_entry.overall_mood
            },
            "mood_variance": round(variance, 2),
            "total_entries": len(moods)
        }
    
    async def create_assessment(
        self,
        user_id: uuid.UUID,
        assessment_type: str,
        responses: Dict,
        total_score: int
    ) -> Assessment:
        """Create a standardized assessment"""
        
        # Determine severity based on assessment type and score
        severity = self._calculate_severity(assessment_type, total_score)
        
        # Get previous assessment for comparison
        previous = await self._get_latest_assessment(user_id, assessment_type)
        previous_score = previous.total_score if previous else None
        score_change = total_score - previous_score if previous_score else None
        
        assessment = Assessment(
            user_id=user_id,
            assessment_type=assessment_type,
            total_score=total_score,
            severity_level=severity,
            responses=encryption_manager.encrypt(str(responses)),
            previous_score=previous_score,
            score_change=score_change
        )
        
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment
    
    async def _get_latest_assessment(
        self,
        user_id: uuid.UUID,
        assessment_type: str
    ) -> Optional[Assessment]:
        """Get latest assessment of specified type"""
        
        query = select(Assessment).where(
            and_(
                Assessment.user_id == user_id,
                Assessment.assessment_type == assessment_type
            )
        ).order_by(desc(Assessment.completed_at)).limit(1)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    def _calculate_severity(self, assessment_type: str, score: int) -> str:
        """Calculate severity level based on assessment type and score"""
        
        if assessment_type == "PHQ-9":
            if score <= 4:
                return "minimal"
            elif score <= 9:
                return "mild"
            elif score <= 14:
                return "moderate"
            elif score <= 19:
                return "moderately_severe"
            else:
                return "severe"
        
        elif assessment_type == "GAD-7":
            if score <= 4:
                return "minimal"
            elif score <= 9:
                return "mild"
            elif score <= 14:
                return "moderate"
            else:
                return "severe"
        
        return "unknown"
