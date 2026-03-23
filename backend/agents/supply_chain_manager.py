from backend.agents.base import BaseAgent
import json

class SupplyChainManager(BaseAgent):
    def __init__(self):
        prompt = "你是一位经验丰富的医药供应链经理。请根据提供的药品存储和运输要求，结合当前的运输与储存成本，评估成本合理性并提出供应链优化建议。"
        super().__init__(name="supply_chain_manager", role="Supply Chain Manager", system_prompt=prompt)
        
    def process_message(self, data: dict):
        session_id = data.get("session_id")
        context = data.get("context", [])
        cost_data = data.get("cost_data", {})
        
        print(f"[{self.name}] Analyzing supply chain for session {session_id}...")
        
        query = f"请结合以下成本数据评估供应链合理性并提出优化建议：\n{json.dumps(cost_data, ensure_ascii=False)}"
        
        response = self.llm.generate(query, context)
        
        result = {
            "optimization": response,
        }
        
        self.publish_result(session_id, result, "event.supplychain.completed")

agent = SupplyChainManager()
