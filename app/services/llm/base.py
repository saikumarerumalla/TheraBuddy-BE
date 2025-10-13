"""Base LLM service interface"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class LLMMessage:
    """Message format for LLM"""
    role: str  # system, user, assistant
    content: str


@dataclass
class LLMResponse:
    """LLM response structure"""
    content: str
    model: str
    tokens_used: int
    response_time_ms: int
    finish_reason: str


class BaseLLMService(ABC):
    """Abstract base class for LLM services"""
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    async def stream_response(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Stream response from LLM"""
        pass
