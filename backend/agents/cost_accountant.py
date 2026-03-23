from backend.agents.base import BaseAgent
import json

class CostAccountant(BaseAgent):
    def __init__(self):
        prompt = "你是一位专业的医药制造成本会计。请基于提供的药品知识和成本数据，详细计算该药品的各项成本占比，并指出成本控制的关键点。"
        super().__init__(name="cost_accountant", role="Cost Accountant", system_prompt=prompt)
        
    def process_message(self, data: dict):
        session_id = data.get("session_id")
        cost_data = data.get("cost_data", {})
        context = data.get("context", [])
        
        print(f"[{self.name}] Analyzing cost data for session {session_id}...")
        
        # Build query
        query = f"请结合以下成本数据对该药品进行全面的成本与市场分析：\n{json.dumps(cost_data, ensure_ascii=False)}"
        
        # Use LLM
        response = self.llm.generate(query, context)
        
        # Calculate total cost including custom costs
        total_cost = 0
        for k, v in cost_data.items():
            if isinstance(v, (int, float)):
                total_cost += v
            elif k == "custom_costs" and isinstance(v, list):
                for custom_item in v:
                    total_cost += custom_item.get("value", 0)
                    
        result = {
            "summary": response,
            "metrics": {"total_cost": total_cost, "cost_tier": "A" if total_cost > 100 else "B"},
            "bottom_line": total_cost * 1.1 # 10% margin as mock bottom line for pricing
        }
        
        self.publish_result(session_id, result, "event.analysis.completed")

agent = CostAccountant()
