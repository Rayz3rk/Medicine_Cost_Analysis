import os
import sys
import requests
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.engine import DrugRAGSystem
from rag.llm_client import BaseLLM, SiliconFlowLLM, OllamaLLM, LocalOpenAILLM
from rag.multi_agent import MultiAgentSystem
from vector.vector_store import ChromaVectorStore

# Load environment variables
load_dotenv()

# Configuration
DRUG_NAME = "二甲双胍恩格列净片(Ⅰ)"
JSONL_FILE = "二甲双胍恩格列净片(Ⅰ).jsonl"
DB_BASE_PATH = "vector_dbs"
# Adjust model path if needed or use environment variable
MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", "D:/models/all-MiniLM-L6-v2")

def get_llm_factory(preferred_provider: str = None):
    """Returns a factory function that creates LLM instances."""
    
    # Check providers logic (simplified version of get_llm)
    def factory():
        # 1. Check preferred provider
        if preferred_provider == "local":
            return LocalOpenAILLM()
        elif preferred_provider == "siliconflow":
             sf_key = os.getenv("SILICONFLOW_API_KEY")
             if sf_key and sf_key.strip() != "your_api_key_here":
                 return SiliconFlowLLM(api_key=sf_key)
        elif preferred_provider == "ollama":
             # Simplified Ollama check
             return OllamaLLM() # Default model

        # 2. Default logic
        sf_key = os.getenv("SILICONFLOW_API_KEY")
        if sf_key and sf_key.strip() != "your_api_key_here":
            return SiliconFlowLLM(api_key=sf_key)
            
        return OllamaLLM() # Fallback to Ollama default

    return factory

def main():
    # 1. Setup
    print(f"初始化 RAG 多智能体系统: {DRUG_NAME}")
    
    # Ensure DB directory exists
    if not os.path.exists(DB_BASE_PATH):
        os.makedirs(DB_BASE_PATH)
        
    jsonl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), JSONL_FILE)
    
    # Check for command line preference
    preferred_provider = sys.argv[1] if len(sys.argv) > 1 else None

    # Initialize LLM Factory
    llm_factory = get_llm_factory(preferred_provider)
    
    # Initialize RAG System (using a default LLM for ingestion/retrieval if needed)
    # Note: RAG system uses LLM for final answer generation. 
    # In multi-agent setup, we might want agents to query the RAG system themselves 
    # or pass retrieved context to agents.
    # For now, let's keep the RAG system as a tool for retrieval.
    default_llm = llm_factory()
    rag_system = DrugRAGSystem(
        drug_name=DRUG_NAME,
        jsonl_path=jsonl_path,
        db_base_path=DB_BASE_PATH,
        model_path=MODEL_PATH,
        llm=default_llm 
    )
    
    # 2. Build Knowledge Base (Ingest)
    print("\n--- 步骤 1: 构建向量知识库 ---")
    if os.path.exists(jsonl_path):
        # 使用 clear_existing=True 来覆盖构建
        rag_system.vector_store.ingest_from_jsonl(jsonl_path, batch_size=50, clear_existing=True)
    else:
        print(f"警告: 找不到数据文件 {jsonl_path}，跳过构建步骤。")

    # 3. 收集成本分析数据
    print("\n--- 请输入成本分析参数 ---")
    print("选择计量单位:")
    print("1: 元/100片")
    print("2: 元/剂")
    print("3: 元/盒")
    unit_choice = input("请输入选项(1/2/3) [默认: 3]: ").strip()
    unit = "元/盒"
    if unit_choice == '1': unit = "元/100片"
    elif unit_choice == '2': unit = "元/剂"
    
    print(f"\n请输入各项成本 ({unit})，直接回车使用默认值0：")
    
    def get_cost(prompt):
        val = input(prompt).strip()
        try:
            return float(val) if val else 0.0
        except ValueError:
            return 0.0

    # 生产成本
    print("\n[生产成本]")
    raw_material_cost = get_cost("原料成本: ")
    rd_cost = get_cost("研发成本 [默认 0]: ")
    production_cost = get_cost("生产工艺成本 [默认 0]: ")
    equipment_cost = get_cost("设备折旧及维护成本 [默认 0]: ")
    
    # 运输成本
    print("\n[运输成本]")
    vehicle_cost = get_cost("车辆设备成本 [默认 0]: ")
    fuel_cost = get_cost("燃料成本 [默认 0]: ")
    
    # 储存成本
    print("\n[储存成本]")
    inventory_loss_cost = get_cost("库存损耗成本 [默认 0]: ")
    warehouse_rent = get_cost("仓储场地租金 [默认 0]: ")
    energy_cost = get_cost("场地能耗成本 [默认 0]: ")
    
    # 其他成本
    print("\n[其他成本]")
    other_cost_name = input("其他成本名称 [可选]: ").strip()
    other_cost_value = 0.0
    if other_cost_name:
        other_cost_value = get_cost(f"{other_cost_name} 成本 [默认 0]: ")

    cost_info = f"""
【成本数据】(单位: {unit})
1. 生产成本:
   - 原料成本: {raw_material_cost}
   - 研发成本: {rd_cost}
   - 生产工艺成本: {production_cost}
   - 设备折旧及维护成本: {equipment_cost}
2. 运输成本:
   - 车辆设备成本: {vehicle_cost}
   - 燃料成本: {fuel_cost}
3. 储存成本:
   - 库存损耗成本: {inventory_loss_cost}
   - 仓储场地租金: {warehouse_rent}
   - 场地能耗成本: {energy_cost}
4. 其他成本 ({other_cost_name if other_cost_name else '无'}): {other_cost_value}
"""

    # 4. 定义成本分析智能体提示词
    accountant_prompt = "你是一位专业的医药制造成本会计。请基于提供的药品知识和成本数据，详细计算该药品的各项成本占比，并指出成本控制的关键点。"
    strategist_prompt = "你是一位医药产品定价策略师。请结合药品的适应症等信息及给定的成本数据，制定合理的市场定价策略，并分析盈利空间。"
    supply_chain_prompt = "你是一位经验丰富的医药供应链经理。请根据提供的药品存储和运输要求，结合当前的运输与储存成本，评估成本合理性并提出供应链优化建议。"
    
    # 5. Setup Multi-Agent System
    print("\n--- 步骤 2: 初始化智能体 ---")
    mas = MultiAgentSystem(llm_factory)
    
    # Define Agents
    mas.create_agent("Cost_Accountant", accountant_prompt)
    mas.create_agent("Pricing_Strategist", strategist_prompt)
    mas.create_agent("Supply_Chain_Manager", supply_chain_prompt)

    # 6. Multi-Agent Chat Loop
    print("\n--- 步骤 3: 多智能体成本分析 ---")
    query = f"请结合以下成本数据对该药品进行全面的成本与市场分析：\n{cost_info}"
    
    # Retrieve Context ONCE
    print("\n[RAG 系统] 正在检索相关知识...")
    rag_query = "该药品的成分、适应症、存储条件和包装规格是什么？"
    search_results = rag_system.query_knowledge(rag_query, top_k=5)
    documents = search_results.get('documents', [[]])[0]
    
    # Let each agent answer based on the SAME context
    agents_to_run = ["Cost_Accountant", "Pricing_Strategist", "Supply_Chain_Manager"]
    
    for agent_name in agents_to_run:
        print(f"\n--- {agent_name} 回答 ---")
        
        # We need to manually format the prompt with context for the agent
        # Or we can use the RAG prompt template if we want consistent formatting
        # For simplicity, let's pass the raw documents as context list to the agent's generate method
        # But wait, our MultiAgentSystem.chat calls agent.generate(query, context)
        # And our LLM classes (SiliconFlowLLM/OllamaLLM) handle context formatting!
        
        response = mas.chat(agent_name, query, context=documents)
        print(f"[{agent_name}]:\n{response}\n")

if __name__ == "__main__":
    main()
