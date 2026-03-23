from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from backend.core.config import settings

# JWT Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# AES-256-GCM Encryption
def encrypt_data(data: str) -> str:
    key = settings.AES_KEY.encode('utf-8')
    if len(key) != 32:
        key = key.ljust(32, b'\0')[:32]
    
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    
    # Store nonce, tag, and ciphertext together
    result = cipher.nonce + tag + ciphertext
    return base64.b64encode(result).decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    key = settings.AES_KEY.encode('utf-8')
    if len(key) != 32:
        key = key.ljust(32, b'\0')[:32]
        
    data = base64.b64decode(encrypted_data)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode('utf-8')
    except ValueError:
        return ""
