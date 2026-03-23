from backend.core.events import create_event
from backend.db.redis_client import redis_bus
import json
import sys
import os

# Ensure the root path is accessible to import rag modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rag.llm_client import SiliconFlowLLM, OllamaLLM
from backend.core.config import settings

def get_llm():
    sf_key = settings.SILICONFLOW_API_KEY
    if sf_key and sf_key.strip() != "your_api_key_here":
        return SiliconFlowLLM(api_key=sf_key)
    return OllamaLLM()

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.channel_sub = f"agent:{self.name}:tasks"
        self.channel_pub = "orchestrator:events"
        
        # Initialize LLM for this agent
        self.llm = get_llm()
        if hasattr(self.llm, 'system_prompt'):
            self.llm.system_prompt = self.system_prompt
        
    def process_message(self, message: dict):
        raise NotImplementedError("Subclasses must implement this method")
        
    def publish_result(self, session_id: str, result: dict, event_type: str):
        event = create_event(
            source=f"agent:{self.name}",
            event_type=event_type,
            data={"session_id": session_id, "result": result}
        )
        redis_bus.publish(self.channel_pub, event.dict())

