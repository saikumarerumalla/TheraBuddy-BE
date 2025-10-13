from datetime import datetime, timedelta
from typing import Dict, List
import pytz


def get_japan_time() -> datetime:
    japan_tz = pytz.timezone('Asia/Tokyo')
    return datetime.now(japan_tz)


def calculate_streak(dates: List[datetime]) -> int:
    if not dates:
        return 0
    
    sorted_dates = sorted(dates, reverse=True)
    streak = 1
    
    for i in range(len(sorted_dates) - 1):
        diff = (sorted_dates[i].date() - sorted_dates[i + 1].date()).days
        if diff == 1:
            streak += 1
        else:
            break
    
    return streak


def format_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
