from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class CustomCost(BaseModel):
    name: str
    value: float
    category: str = "其他成本"

class CostData(BaseModel):
    raw_material_cost: float = Field(..., description="原料成本")
    rd_cost: float = Field(0, description="研发成本")
    production_cost: float = Field(0, description="生产工艺成本")
    equipment_cost: float = Field(0, description="设备折旧及维护成本")
    
    vehicle_cost: float = Field(0, description="车辆设备成本")
    fuel_cost: float = Field(0, description="燃料成本")
    
    inventory_loss_cost: float = Field(0, description="库存损耗成本")
    warehouse_rent: float = Field(0, description="仓储场地租金")
    energy_cost: float = Field(0, description="场地能耗成本")
    
    custom_costs: List[CustomCost] = Field(default_factory=list, description="自定义成本项")

class AnalysisRequest(BaseModel):
    drug_name: str
    unit: str = Field(default="元/盒", description="计量单位：元/100片, 元/剂, 元/盒")
    costs: CostData

class DrugCreate(BaseModel):
    name: str
    specifications: Optional[str] = None
    indications: Optional[str] = None
    storage_conditions: Optional[str] = None

class DrugUpdate(DrugCreate):
    pass

class DrugResponse(DrugCreate):
    id: str
    created_at: datetime
    updated_at: datetime
