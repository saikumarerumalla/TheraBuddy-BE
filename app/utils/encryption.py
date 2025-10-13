"""Data encryption utilities for sensitive information"""

from cryptography.fernet import Fernet
from app.config import get_settings
import base64

settings = get_settings()


class EncryptionManager:
    """Handle encryption/decryption of sensitive data"""
    
    def __init__(self):
        # Ensure key is properly formatted
        key = settings.ENCRYPTION_KEY.encode()
        if len(key) != 44:  # Fernet keys are 44 bytes in base64
            key = base64.urlsafe_b64encode(key.ljust(32)[:32])
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        if not data:
            return ""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        if not encrypted_data:
            return ""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()


encryption_manager = EncryptionManager()
