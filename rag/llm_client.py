import os
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

class BaseLLM(ABC):
    """Abstract base class for LLM clients."""
    @abstractmethod
    def generate(self, prompt: str, context: List[str] = []) -> str:
        """Generates a response given a prompt and context."""
        pass

class SiliconFlowLLM(BaseLLM):
    """LLM client for SiliconFlow API (OpenAI compatible)."""
    def __init__(self, api_key: str = None, model: str = "Qwen/Qwen3-8B", base_url: str = "https://api.siliconflow.cn/v1", system_prompt: str = "你是一个有用的助手。请使用提供的上下文来回答用户的问题。"):
        self.api_key = api_key or os.getenv("SILICONFLOW_API_KEY")
        if not self.api_key:
            print("Warning: SILICONFLOW_API_KEY not found in environment variables.")
        self.model = model
        self.base_url = base_url
        self.system_prompt = system_prompt
        
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    def generate(self, prompt: str, context: List[str] = []) -> str:
        if not self.client:
            return "Error: SiliconFlow API key is missing. Please set SILICONFLOW_API_KEY in .env file."

        # If context is provided, append it to the user message. 
        # If the caller already embedded context in 'prompt', they should pass context=[]
        full_user_content = prompt
        if context:
            context_str = "\n".join(context)
            full_user_content = f"Context:\n{context_str}\n\nQuestion: {prompt}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": full_user_content}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling SiliconFlow API: {e}"

class OllamaLLM(BaseLLM):
    """LLM client for Ollama local models."""
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3.5:0.8b", system_prompt: str = "你是一个有用的助手。"):
        self.base_url = base_url
        self.model = model
        self.system_prompt = system_prompt

    def generate(self, prompt: str, context: List[str] = []) -> str:
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context:\n{context_str}\n\nQuestion: {prompt}"
        
        url = f"{self.base_url}/api/chat"
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result['message']['content']
        except requests.exceptions.RequestException as e:
            return f"Error calling Ollama API: {e}. Make sure Ollama is running."
        except (KeyError, IndexError) as e:
            return f"Error parsing Ollama response: {e}"

class LocalOpenAILLM(BaseLLM):
    """LLM client for locally deployed models with OpenAI compatible API (e.g., vLLM, LMStudio)."""
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "local-model", api_key: str = "EMPTY", system_prompt: str = "你是一个有用的助手。请使用提供的上下文来回答用户的问题。"):
        self.base_url = base_url
        self.model = model
        self.api_key = api_key
        self.system_prompt = system_prompt
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate(self, prompt: str, context: List[str] = []) -> str:
        full_user_content = prompt
        if context:
            context_str = "\n".join(context)
            full_user_content = f"Context:\n{context_str}\n\nQuestion: {prompt}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": full_user_content}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling Local OpenAI API: {e}"

class SimpleLLM(BaseLLM):
    """A placeholder for backward compatibility, defaults to Mock behavior if no key."""
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, context: List[str] = []) -> str:
        return f"[SimpleLLM Placeholder] Would call {self.model} with prompt: {prompt}"
