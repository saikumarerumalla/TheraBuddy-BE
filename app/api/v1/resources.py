from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User
from typing import List, Dict

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/crisis")
async def get_crisis_resources(
    current_user: User = Depends(get_current_user)
) -> Dict:
    return {
        "hotlines": [
            {
                "name": "988 Suicide & Crisis Lifeline",
                "phone": "988",
                "hours": "24/7",
                "website": "https://988lifeline.org"
            },
            {
                "name": "Crisis Text Line",
                "phone": "Text HOME to 741741",
                "hours": "24/7"
            }
        ],
        "emergency": {
            "police": "911",
            "ambulance": "911"
        }
    }


@router.get("/articles")
async def get_educational_articles(
    category: str = None,
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    articles = [
        {
            "id": "understanding-anxiety",
            "title": "Understanding Anxiety",
            "category": "anxiety",
            "read_time_minutes": 5
        },
        {
            "id": "cbt-basics",
            "title": "Introduction to CBT",
            "category": "education",
            "read_time_minutes": 10
        }
    ]
    
    if category:
        articles = [a for a in articles if a["category"] == category]
    
    return articles
