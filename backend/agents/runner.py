import threading
import json
from backend.db.redis_client import redis_bus
from backend.agents.cost_accountant import agent as cost_agent
from backend.agents.pricing_strategist import agent as pricing_agent
from backend.agents.supply_chain_manager import agent as sc_agent
from backend.agents.orchestrator import run_orchestrator_listener

def agent_listener(agent_instance):
    pubsub = redis_bus.subscribe(agent_instance.channel_sub)
    for message in pubsub.listen():
        if message['type'] == 'message':
            event_data = json.loads(message['data'])
            agent_instance.process_message(event_data.get("data", {}))

def start_all_agents():
    threads = [
        threading.Thread(target=run_orchestrator_listener, daemon=True),
        threading.Thread(target=agent_listener, args=(cost_agent,), daemon=True),
        threading.Thread(target=agent_listener, args=(pricing_agent,), daemon=True),
        threading.Thread(target=agent_listener, args=(sc_agent,), daemon=True),
    ]
    for t in threads:
        t.start()
    print("All agent listeners started.")
