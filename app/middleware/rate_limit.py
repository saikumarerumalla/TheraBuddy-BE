from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.cache import cache_manager
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period

    async def dispatch(self, request: Request, call_next):
        # Get client identifier (IP or user ID)
        client_id = request.client.host
        
        # Check authorization header for user ID
        auth_header = request.headers.get("authorization")
        if auth_header:
            # Use user ID instead of IP if authenticated
            # This is simplified - in production, decode the token
            client_id = auth_header
        
        # Rate limit key
        key = f"rate_limit:{client_id}"
        
        # Get current count
        current_count = await cache_manager.get(key)
        
        if current_count is None:
            await cache_manager.set(key, 1, expire=self.period)
        elif int(current_count) >= self.calls:
            raise HTTPException(status_code=429, detail="Too many requests")
        else:
            await cache_manager.set(key, int(current_count) + 1, expire=self.period)
        
        response = await call_next(request)
        return response
