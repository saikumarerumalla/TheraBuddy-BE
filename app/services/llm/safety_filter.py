"""Safety filtering and crisis detection"""

import re
from typing import Dict, Tuple, List
from app.config import get_settings

settings = get_settings()


class SafetyFilter:
    """Detect crisis keywords and assess risk level"""
    
    # Crisis keywords with severity levels
    CRISIS_KEYWORDS = {
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
    def detect_crisis(text: str) -> Tuple[bool, str, List[str]]:
        """
        Detect crisis keywords in text
        
        Returns:
            (is_crisis, risk_level, detected_keywords)
        """
        
        text_lower = text.lower()
        keywords_dict = SafetyFilter.CRISIS_KEYWORDS
        
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
        positive_words = ["happy", "good", "great", "better", "wonderful", "excited", "grateful", "hopeful"]
        negative_words = ["sad", "bad", "terrible", "worse", "awful", "hopeless", "miserable", "depressed"]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total
        return max(-1.0, min(1.0, sentiment))
