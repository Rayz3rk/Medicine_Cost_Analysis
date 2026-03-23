import os
import json
import time
from typing import Dict, Any, List
from .llm_client import BaseLLM

class MultiAgentSystem:
    def __init__(self, llm_factory):
        """
        Initialize the multi-agent system.
        
        Args:
            llm_factory: A function that returns a new LLM instance. 
                         This is used to create separate LLM instances for each agent if needed,
                         or reconfigure them with different system prompts.
        """
        self.llm_factory = llm_factory
        self.agents: Dict[str, BaseLLM] = {}
        self.agent_configs: Dict[str, str] = {} # agent_name -> system_prompt
        self.history_dir = "chat_history"
        
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def create_agent(self, name: str, system_prompt: str):
        """
        Creates a new agent with a specific system prompt.
        
        Args:
            name: The name of the agent (e.g., "Doctor", "Pharmacist").
            system_prompt: The system prompt defining the agent's persona and behavior.
        """
        self.agent_configs[name] = system_prompt
        # Create a new LLM instance for this agent
        # We assume llm_factory can accept a system_prompt argument if it's our custom classes
        # Or we manually set it after creation if possible.
        
        # Here we instantiate a new LLM client. 
        # Note: Ideally, our LLM classes should support dynamic system prompt updates or 
        # we create new instances. Let's assume we create new instances.
        
        # To make this flexible, we'll ask the factory for an instance, 
        # then try to set its system_prompt attribute if it exists.
        llm = self.llm_factory()
        
        if hasattr(llm, 'system_prompt'):
            llm.system_prompt = system_prompt
        else:
            print(f"Warning: LLM client for agent '{name}' does not support setting system_prompt attribute directly.")
            
        self.agents[name] = llm
        print(f"Agent '{name}' created.")

    def get_agent(self, name: str) -> BaseLLM:
        return self.agents.get(name)

    def save_response(self, agent_name: str, user_query: str, response: str, metadata: Dict[str, Any] = None):
        """
        Saves the agent's response to a file.
        
        Args:
            agent_name: Name of the agent.
            user_query: The input query.
            response: The agent's response.
            metadata: Additional metadata (optional).
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.history_dir}/response_{timestamp}_{agent_name}.json"
        
        data = {
            "timestamp": timestamp,
            "agent_name": agent_name,
            "system_prompt": self.agent_configs.get(agent_name),
            "user_query": user_query,
            "response": response,
            "metadata": metadata or {}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Response saved to {filename}")

    def chat(self, agent_name: str, query: str, context: List[str] = []) -> str:
        """
        Sends a query to a specific agent and gets a response.
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return f"Error: Agent '{agent_name}' not found."
            
        print(f"[{agent_name}] is thinking...")
        response = agent.generate(query, context)
        
        # Save automatically? Or let caller decide?
        # Let's save it automatically for convenience as requested.
        self.save_response(agent_name, query, response)
        
        return response
