from backend.agents.base import BaseAgent
import json

class PricingStrategist(BaseAgent):
    def __init__(self):
        prompt = "你是一位医药产品定价策略师。请结合药品的适应症等信息及给定的成本数据，制定合理的市场定价策略，并分析盈利空间。"
        super().__init__(name="pricing_strategist", role="Pricing Strategist", system_prompt=prompt)
        
    def process_message(self, data: dict):
        session_id = data.get("session_id")
        accountant_result = data.get("accountant_result", {})
        context = data.get("context", [])
        cost_data = data.get("cost_data", {})
        
        print(f"[{self.name}] Calculating pricing strategy for session {session_id}...")
        
        query = f"前期成本会计的分析结果如下：\n{accountant_result.get('summary', '')}\n请结合原始成本数据 {json.dumps(cost_data, ensure_ascii=False)} 制定定价策略。"
        
        response = self.llm.generate(query, context)
        
        bottom_line = accountant_result.get("bottom_line", 0)
        target_price = bottom_line * 1.5 # Mock numerical output
        
        result = {
            "strategy": response,
            "target_price": target_price,
            "margin": target_price - bottom_line
        }
        
        self.publish_result(session_id, result, "event.pricing.completed")

agent = PricingStrategist()
