import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock before importing app
sys.modules['rag.engine'] = MagicMock()

from fastapi.testclient import TestClient
from backend.main import app
from bson import ObjectId

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Multi-Agent Backend is running"}

@patch("backend.api.routes.get_mongo_db")
def test_drug_crud_mock(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    
    mock_db.drugs.insert_one.return_value.inserted_id = ObjectId("507f1f77bcf86cd799439011")
    
    response = client.post("/api/v1/drugs", json={
        "name": "Test Drug",
        "specifications": "100mg"
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "Test Drug"
    assert response.json()["id"] == "507f1f77bcf86cd799439011"
