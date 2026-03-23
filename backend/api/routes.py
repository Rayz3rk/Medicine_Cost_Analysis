from fastapi import APIRouter, HTTPException, Depends
from typing import List
from backend.agents.orchestrator import orchestrator
from backend.db.redis_client import get_redis
from backend.db.mongo_client import get_mongo_db
from backend.api.models import AnalysisRequest, DrugCreate, DrugUpdate, DrugResponse
import json
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/analyze")
async def start_analysis(request: AnalysisRequest):
    task_data = request.dict()
    session_id = orchestrator.start_session(task_data)
    return {"session_id": session_id, "status": "started", "message": "Analysis tasks dispatched"}

@router.get("/status/{session_id}")
async def get_status(session_id: str):
    redis = get_redis()
    status = redis.hget(f"session:{session_id}", "status")
    
    if not status:
        raise HTTPException(status_code=404, detail="Session not found")
        
    if status == "completed":
        report_raw = redis.hget(f"session:{session_id}", "report")
        report = json.loads(report_raw) if report_raw else {}
        return {"session_id": session_id, "status": status, "report": report}
        
    return {"session_id": session_id, "status": status}

# Drug CRUD API
@router.post("/drugs", response_model=DrugResponse)
async def create_drug(drug: DrugCreate):
    db = get_mongo_db()
    drug_dict = drug.dict()
    drug_dict["created_at"] = datetime.utcnow()
    drug_dict["updated_at"] = datetime.utcnow()
    
    result = db.drugs.insert_one(drug_dict)
    drug_dict["id"] = str(result.inserted_id)
    return drug_dict

@router.get("/drugs", response_model=List[DrugResponse])
async def list_drugs():
    db = get_mongo_db()
    drugs = []
    for doc in db.drugs.find():
        doc["id"] = str(doc.pop("_id"))
        drugs.append(doc)
    return drugs

@router.get("/drugs/{drug_id}", response_model=DrugResponse)
async def get_drug(drug_id: str):
    db = get_mongo_db()
    doc = db.drugs.find_one({"_id": ObjectId(drug_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Drug not found")
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.put("/drugs/{drug_id}", response_model=DrugResponse)
async def update_drug(drug_id: str, drug: DrugUpdate):
    db = get_mongo_db()
    update_data = drug.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = db.drugs.update_one({"_id": ObjectId(drug_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Drug not found")
        
    return await get_drug(drug_id)

@router.delete("/drugs/{drug_id}")
async def delete_drug(drug_id: str):
    db = get_mongo_db()
    result = db.drugs.delete_one({"_id": ObjectId(drug_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Drug not found")
    return {"message": "Drug deleted successfully"}
