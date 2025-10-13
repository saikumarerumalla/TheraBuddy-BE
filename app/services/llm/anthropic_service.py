"""Anthropic Claude service implementation"""

import time
from typing import List
from anthropic import AsyncAnthropic
from app.services.llm.base import BaseLLMService, LLMMessage, LLMResponse
from app.config import get_settings

settings = get_settings()


class AnthropicService(BaseLLMService):
    """Anthropic Claude service implementation"""
    
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_response(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate response from Anthropic Claude"""
        
        start_time = time.time()
        
        # Separate system message from other messages
        system_message = ""
        formatted_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        response = await self.client.messages.create(
            model=self.model,
            system=system_message,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            response_time_ms=response_time_ms,
            finish_reason=response.stop_reason
        )
    
    async def stream_response(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Stream response from Anthropic Claude"""
        
        system_message = ""
        formatted_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        async with self.client.messages.stream(
            model=self.model,
            system=system_message,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        ) as stream:
            async for text in stream.text_stream:
                yield text
