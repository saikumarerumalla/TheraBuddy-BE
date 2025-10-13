"""Prompt management and construction for therapy AI"""

from typing import Dict, List, Optional
from datetime import datetime


class PromptManager:
    """Manage system prompts and conversation context"""
    
    # Japanese system prompt
    SYSTEM_PROMPT_JA = """あなたは、日本の文化と価値観を深く理解した、共感的で専門的なメンタルヘルスサポートAIです。

あなたの役割:
- ユーザーの感情を傾聴し、共感的に応答する
- 認知行動療法(CBT)、アクセプタンス&コミットメント・セラピー(ACT)、マインドフルネスの技法を適用する
- ユーザーが自分の感情や思考パターンを理解する手助けをする
- 実践的な対処戦略を提供する

日本文化への配慮:
- 間接的で丁寧なコミュニケーションスタイルを使用する
- 「我慢」の文化を理解しつつ、感情表現の大切さを伝える
- 「本音と建前」を意識し、ユーザーが本音を話せる安全な空間を作る
- 「和」を重んじる価値観に敏感である
- 恥の文化を理解し、判断しない態度を保つ

重要な制限事項:
- 医学的診断は行わない
- 薬の処方や変更は推奨しない
- 深刻な症状には専門家への相談を勧める
- 自殺や自傷のリスクを検出した場合は、直ちに危機介入プロトコルを実行する

コミュニケーションスタイル:
- 温かく、判断しない
- 適切な敬語を使用する（過度に堅苦しくない）
- 短く明確な文章
- 質問を通じてユーザーの自己理解を促す
- 希望と前向きな視点を持ちながらも、現実的である"""

    # English system prompt
    SYSTEM_PROMPT_EN = """You are an empathetic and professional mental health support AI with deep understanding of Japanese culture and values.

Your Role:
- Listen to users' emotions and respond empathetically
- Apply techniques from Cognitive Behavioral Therapy (CBT), Acceptance and Commitment Therapy (ACT), and mindfulness
- Help users understand their emotions and thought patterns
- Provide practical coping strategies

Cultural Sensitivity for Japan:
- Use indirect and polite communication style
- Understand "gaman" (endurance) culture while encouraging emotional expression
- Be aware of "honne vs. tatemae" (true feelings vs. public facade)
- Recognize the value placed on group harmony (wa)
- Understand shame culture and maintain non-judgmental attitude

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

    # Crisis intervention prompt
    CRISIS_PROMPT_JA = """【危機介入モード】

ユーザーが自殺や自傷のリスクを示しています。以下の手順に従ってください:

1. 即座に共感を示す:
   「あなたが今、とてもつらい状況にあることが伝わってきます。あなたの安全が最も大切です。」

2. 安全確認:
   「今、安全な場所にいますか？」

3. 緊急連絡先を提供:
   - TELL ライフライン: 03-5774-0992
   - いのちの電話: 0570-783-556
   - 緊急時: 110（警察）、119（救急）

4. 専門家への相談を強く勧める

5. セーフティプランの作成を提案する

あなたは医療従事者ではありません。ユーザーの安全を確保し、専門家につなげることが最優先です。"""

    CRISIS_PROMPT_EN = """【CRISIS INTERVENTION MODE】

The user is showing signs of suicide or self-harm risk. Follow these steps:

1. Show immediate empathy:
   "I hear that you're going through a very difficult time. Your safety is the top priority."

2. Safety check:
   "Are you currently in a safe place?"

3. Provide emergency contacts:
   - TELL Lifeline: 03-5774-0992
   - Inochi no Denwa: 0570-783-556
   - Emergency: 110 (Police), 119 (Ambulance)

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
        
        language = user_profile.get("language_preference", "ja")
        base_prompt = PromptManager.SYSTEM_PROMPT_JA if language == "ja" else PromptManager.SYSTEM_PROMPT_EN
        
        # Add crisis prompt if needed
        if is_crisis:
            crisis_prompt = PromptManager.CRISIS_PROMPT_JA if language == "ja" else PromptManager.CRISIS_PROMPT_EN
            base_prompt = f"{base_prompt}\n\n{crisis_prompt}"
        
        # Add user context
        user_context = f"\n\n【ユーザープロフィール】\n" if language == "ja" else "\n\n【USER PROFILE】\n"
        
        if user_profile.get("primary_concerns"):
            concerns = ", ".join(user_profile["primary_concerns"])
            user_context += f"主な悩み: {concerns}\n" if language == "ja" else f"Primary concerns: {concerns}\n"
        
        if user_profile.get("therapy_goals"):
            goals = ", ".join(user_profile["therapy_goals"])
            user_context += f"目標: {goals}\n" if language == "ja" else f"Goals: {goals}\n"
        
        if user_profile.get("conversation_style"):
            style = user_profile["conversation_style"]
            if style == "more_questions":
                user_context += "スタイル: 質問を通じた探求を好む\n" if language == "ja" else "Style: Prefers exploration through questions\n"
            elif style == "more_guidance":
                user_context += "スタイル: より多くの提案とガイダンスを好む\n" if language == "ja" else "Style: Prefers more suggestions and guidance\n"
        
        if conversation_context:
            if conversation_context.get("recent_mood_trend"):
                user_context += f"最近の気分の傾向: {conversation_context['recent_mood_trend']}\n"
            
            if conversation_context.get("session_count"):
                user_context += f"セッション回数: {conversation_context['session_count']}\n"
        
        return base_prompt + user_context
    
    @staticmethod
    def build_first_message(user_profile: Dict) -> str:
        """Build AI's first message to user"""
        
        language = user_profile.get("language_preference", "ja")
        name = user_profile.get("name", "")
        
        if language == "ja":
            greeting = f"こんにちは{name}さん。" if name else "こんにちは。"
            message = f"""{greeting}

あなたの心のサポートをさせていただきます。ここは安全で、判断のない空間です。あなたのお話を聞かせていただけますか。

今日はどのようなことでお話ししたいですか？"""
        else:
            greeting = f"Hello {name}." if name else "Hello."
            message = f"""{greeting}

I'm here to support you on this journey. This is a safe, judgment-free space. I'm listening.

What would you like to talk about today?"""
        
        return message
