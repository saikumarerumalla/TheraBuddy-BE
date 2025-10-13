from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User
from typing import List, Dict

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/crisis")
async def get_crisis_resources(
    language: str = "ja",
    current_user: User = Depends(get_current_user)
) -> Dict:
    if language == "ja":
        return {
            "hotlines": [
                {
                    "name": "TELL ライフライン",
                    "phone": "03-5774-0992",
                    "hours": "毎日 9:00-23:00",
                    "website": "https://telljp.com"
                },
                {
                    "name": "いのちの電話",
                    "phone": "0570-783-556",
                    "hours": "24時間365日"
                }
            ],
            "emergency": {
                "police": "110",
                "ambulance": "119"
            }
        }
    else:
        return {
            "hotlines": [
                {
                    "name": "TELL Lifeline",
                    "phone": "03-5774-0992",
                    "hours": "Daily 9:00-23:00",
                    "website": "https://telljp.com"
                }
            ],
            "emergency": {
                "police": "110",
                "ambulance": "119"
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
            "title_ja": "不安を理解する",
            "category": "anxiety",
            "read_time_minutes": 5
        },
        {
            "id": "cbt-basics",
            "title": "Introduction to CBT",
            "title_ja": "認知行動療法入門",
            "category": "education",
            "read_time_minutes": 10
        }
    ]
    
    if category:
        articles = [a for a in articles if a["category"] == category]
    
    return articles
