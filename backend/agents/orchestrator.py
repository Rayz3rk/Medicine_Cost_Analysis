import json
import uuid
import sys
import os

# Ensure the root path is accessible to import rag modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rag.engine import DrugRAGSystem
from backend.core.events import create_event
from backend.db.redis_client import redis_bus, get_redis
from backend.db.mongo_client import get_mongo_db
from backend.core.security import encrypt_data
from backend.agents.base import get_llm

class Orchestrator:
    def __init__(self):
        self.channel_sub = "orchestrator:events"
        self.redis = get_redis()
        self.mongo = get_mongo_db()
        self.sessions = {} # session_id -> {status, data, results}
        
        # Initialize RAG System
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        drug_name = "二甲双胍恩格列净片(Ⅰ)"
        jsonl_path = os.path.join(base_path, f"{drug_name}.jsonl")
        db_base_path = os.path.join(base_path, "vector_dbs")
        model_path = os.getenv("EMBEDDING_MODEL_PATH", "D:/models/all-MiniLM-L6-v2")
        
        self.rag_system = DrugRAGSystem(
            drug_name=drug_name,
            jsonl_path=jsonl_path,
            db_base_path=db_base_path,
            model_path=model_path,
            llm=get_llm() 
        )
        
    def start_session(self, task_data: dict) -> str:
        session_id = f"session-{uuid.uuid4().hex[:8]}"
        
        # Pre-retrieve context using RAG
        print(f"[{session_id}] Retrieving context from RAG...")
        rag_query = f"{task_data.get('drug_name', '二甲双胍恩格列净片')}的成分、适应症、存储条件和包装规格是什么？"
        search_results = self.rag_system.query_knowledge(rag_query, top_k=5)
        documents = search_results.get('documents', [[]])[0]
        
        self.sessions[session_id] = {
            "status": "started",
            "task_data": task_data,
            "context": documents,
            "results": {}
        }
        
        # 1. Store in Redis (short term)
        self.redis.hset(f"session:{session_id}", "status", "started")
        
        # 2. Dispatch to Cost Accountant first
        event = create_event(
            source="orchestrator",
            event_type="task.cost_analysis",
            data={
                "session_id": session_id, 
                "cost_data": task_data.get("costs", {}),
                "context": documents
            }
        )
        redis_bus.publish("agent:cost_accountant:tasks", event.dict())
        
        return session_id

    def handle_event(self, event_data: dict):
        event_type = event_data.get("type")
        data = event_data.get("data", {})
        session_id = data.get("session_id")
        result = data.get("result")
        
        if not session_id or session_id not in self.sessions:
            return
            
        session = self.sessions[session_id]
        
        if event_type == "event.analysis.completed":
            session["results"]["accountant"] = result
            # Now trigger parallel tasks: Pricing & Supply Chain
            pricing_event = create_event(
                "orchestrator", "task.pricing", 
                {
                    "session_id": session_id, 
                    "accountant_result": result, 
                    "context": session["context"],
                    "cost_data": session["task_data"].get("costs", {})
                }
            )
            sc_event = create_event(
                "orchestrator", "task.supply_chain", 
                {
                    "session_id": session_id, 
                    "context": session["context"],
                    "cost_data": session["task_data"].get("costs", {})
                }
            )
            
            redis_bus.publish("agent:pricing_strategist:tasks", pricing_event.dict())
            redis_bus.publish("agent:supply_chain_manager:tasks", sc_event.dict())
            
        elif event_type == "event.pricing.completed":
            session["results"]["pricing"] = result
            self._check_completion(session_id)
            
        elif event_type == "event.supplychain.completed":
            session["results"]["supply_chain"] = result
            self._check_completion(session_id)

    def _check_completion(self, session_id: str):
        session = self.sessions[session_id]
        results = session["results"]
        
        if "pricing" in results and "supply_chain" in results:
            session["status"] = "completed"
            
            # Here we just combine results. 
            # In a real Map-Reduce, we would use LLM to summarize.
            final_report = {
                "session_id": session_id,
                "cost_summary": results["accountant"]["summary"],
                "pricing_strategy": results["pricing"]["strategy"],
                "supply_chain_advice": results["supply_chain"]["optimization"],
                "status": "completed"
            }
            
            # Save to Redis
            self.redis.hset(f"session:{session_id}", "status", "completed")
            self.redis.hset(f"session:{session_id}", "report", json.dumps(final_report))
            
            # Save to MongoDB (Encrypted)
            try:
                encrypted_report = encrypt_data(json.dumps(final_report))
                self.mongo.sessions.insert_one({
                    "session_id": session_id,
                    "encrypted_data": encrypted_report,
                    "created_at": "now" # simplified
                })
            except Exception as e:
                print(f"Mongo save failed: {e}")

orchestrator = Orchestrator()

def run_orchestrator_listener():
    pubsub = redis_bus.subscribe(orchestrator.channel_sub)
    for message in pubsub.listen():
        if message['type'] == 'message':
            event_data = json.loads(message['data'])
            orchestrator.handle_event(event_data)
