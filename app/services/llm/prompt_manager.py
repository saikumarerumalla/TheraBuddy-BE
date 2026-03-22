"""Prompt management and construction for therapy AI"""

from typing import Dict, List, Optional
from datetime import datetime


class PromptManager:
    """Manage system prompts and conversation context"""
    
    SYSTEM_PROMPT = """You are an empathetic and professional mental health support AI.

Your Role:
- Listen to users' emotions and respond empathetically
- Apply techniques from Cognitive Behavioral Therapy (CBT), Acceptance and Commitment Therapy (ACT), and mindfulness
- Help users understand their emotions and thought patterns
- Provide practical coping strategies

Cultural Sensitivity:
- Be respectful of diverse cultural backgrounds and values
- Encourage emotional expression while respecting individual boundaries
- Create a safe, non-judgmental space for open communication
- Be mindful of personal and cultural differences in coping styles

Important Limitations:
- Do not provide medical diagnoses
- Do not recommend medication or changes to prescriptions
- Refer serious symptoms to professional help
- Execute crisis intervention protocol immediately if suicide or self-harm risk is detected

Communication Style:
- Warm and non-judgmental
- Use appropriate respectful language (not overly formal)
- Keep responses concise and clear
- Use questions to facilitate user's self-understanding
- Maintain hope and positive perspective while being realistic"""

    CRISIS_PROMPT = """【CRISIS INTERVENTION MODE】

The user is showing signs of suicide or self-harm risk. Follow these steps:

1. Show immediate empathy:
   "I hear that you're going through a very difficult time. Your safety is the top priority."

2. Safety check:
   "Are you currently in a safe place?"

3. Provide emergency contacts:
   - 988 Suicide & Crisis Lifeline: 988 (call or text, 24/7)
   - Crisis Text Line: Text HOME to 741741
   - Emergency: 911

4. Strongly encourage professional help

5. Offer to create a safety plan

You are not a medical professional. Ensuring user safety and connecting them to professionals is the top priority."""

    @staticmethod
    def build_system_prompt(
        user_profile: Dict,
        conversation_context: Optional[Dict] = None,
        is_crisis: bool = False
    ) -> str:
        """Build system prompt based on user profile and context"""
        
        base_prompt = PromptManager.SYSTEM_PROMPT
        
        # Add crisis prompt if needed
        if is_crisis:
            base_prompt = f"{base_prompt}\n\n{PromptManager.CRISIS_PROMPT}"
        
        # Add user context
        user_context = "\n\n【USER PROFILE】\n"
        
        if user_profile.get("primary_concerns"):
            concerns = ", ".join(user_profile["primary_concerns"])
            user_context += f"Primary concerns: {concerns}\n"
        
        if user_profile.get("therapy_goals"):
            goals = ", ".join(user_profile["therapy_goals"])
            user_context += f"Goals: {goals}\n"
        
        if user_profile.get("conversation_style"):
            style = user_profile["conversation_style"]
            if style == "more_questions":
                user_context += "Style: Prefers exploration through questions\n"
            elif style == "more_guidance":
                user_context += "Style: Prefers more suggestions and guidance\n"
        
        if conversation_context:
            if conversation_context.get("recent_mood_trend"):
                user_context += f"Recent mood trend: {conversation_context['recent_mood_trend']}\n"
            
            if conversation_context.get("session_count"):
                user_context += f"Session count: {conversation_context['session_count']}\n"
        
        return base_prompt + user_context
    
    @staticmethod
    def build_first_message(user_profile: Dict) -> str:
        """Build AI's first message to user"""
        
        name = user_profile.get("name", "")
        
        greeting = f"Hello {name}." if name else "Hello."
        message = f"""{greeting}

I'm here to support you on this journey. This is a safe, judgment-free space. I'm listening.

What would you like to talk about today?"""
        
        return message
