"""Safety filtering and crisis detection"""

import re
from typing import Dict, Tuple, List
from app.config import get_settings

settings = get_settings()


class SafetyFilter:
    """Detect crisis keywords and assess risk level"""
    
    # Crisis keywords with severity levels
    CRISIS_KEYWORDS_JA = {
        "critical": [
            "今すぐ死にたい", "今から死ぬ", "遺書", "自殺する",
            "飛び降り", "首を吊", "薬を飲む", "今日死"
        ],
        "high": [
            "死にたい", "消えたい", "終わりにしたい", "自殺",
            "生きる価値", "死ぬ方法", "楽に死ね"
        ],
        "medium": [
            "疲れた", "もう無理", "限界", "助けて",
            "辛すぎる", "耐えられない", "消えてしまいたい"
        ]
    }
    
    CRISIS_KEYWORDS_EN = {
        "critical": [
            "kill myself now", "going to die", "suicide note",
            "end it today", "jump off", "hang myself"
        ],
        "high": [
            "want to die", "suicide", "kill myself",
            "end my life", "no reason to live", "better off dead"
        ],
        "medium": [
            "can't go on", "give up", "no hope",
            "unbearable", "can't take it", "want to disappear"
        ]
    }
    
    @staticmethod
    def detect_crisis(text: str, language: str = "ja") -> Tuple[bool, str, List[str]]:
        """
        Detect crisis keywords in text
        
        Returns:
            (is_crisis, risk_level, detected_keywords)
        """
        
        text_lower = text.lower()
        keywords_dict = SafetyFilter.CRISIS_KEYWORDS_JA if language == "ja" else SafetyFilter.CRISIS_KEYWORDS_EN
        
        detected = []
        highest_risk = "low"
        
        # Check critical keywords
        for keyword in keywords_dict["critical"]:
            if keyword.lower() in text_lower:
                detected.append(keyword)
                highest_risk = "critical"
        
        # Check high-risk keywords
        if highest_risk != "critical":
            for keyword in keywords_dict["high"]:
                if keyword.lower() in text_lower:
                    detected.append(keyword)
                    highest_risk = "high"
        
        # Check medium-risk keywords
        if highest_risk not in ["critical", "high"]:
            for keyword in keywords_dict["medium"]:
                if keyword.lower() in text_lower:
                    detected.append(keyword)
                    if highest_risk == "low":
                        highest_risk = "medium"
        
        is_crisis = len(detected) > 0
        
        return is_crisis, highest_risk, detected
    
    @staticmethod
    def assess_sentiment(text: str) -> float:
        """
        Simple sentiment analysis (-1 to 1)
        In production, use a proper sentiment analysis model
        """
        
        # This is a simplified version - in production, use a proper model
        positive_words = ["嬉しい", "良い", "楽しい", "幸せ", "happy", "good", "great", "better"]
        negative_words = ["悲しい", "辛い", "苦しい", "悪い", "sad", "bad", "terrible", "worse"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total
        return max(-1.0, min(1.0, sentiment))
