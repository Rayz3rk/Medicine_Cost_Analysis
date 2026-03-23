import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Multi-Agent Backend"
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # MongoDB
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "multi_agent_db")
    
    # Neo4j
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-12345678901234567890123456789012")
    ALGORITHM: str = "HS256"
    AES_KEY: str = os.getenv("AES_KEY", "12345678901234567890123456789012") # 32 bytes for AES-256
    
    # LLM
    SILICONFLOW_API_KEY: str = os.getenv("SILICONFLOW_API_KEY", "")

settings = Settings()
