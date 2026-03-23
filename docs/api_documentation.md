# 药品成本分析系统 API 文档

## 1. 基础信息
- **Base URL**: `/api/v1`
- **数据格式**: `application/json`

## 2. 接口列表

### 2.1 药品管理 (Drug Management)

#### 获取药品列表
- **URL**: `/drugs`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "id": "string",
    "name": "string",
    "specifications": "string",
    "indications": "string",
    "storage_conditions": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

#### 创建药品
- **URL**: `/drugs`
- **Method**: `POST`
- **Body**:
```json
{
  "name": "string",
  "specifications": "string",
  "indications": "string",
  "storage_conditions": "string"
}
```

#### 更新药品
- **URL**: `/drugs/{drug_id}`
- **Method**: `PUT`
- **Body**: 同创建药品

#### 删除药品
- **URL**: `/drugs/{drug_id}`
- **Method**: `DELETE`

### 2.2 成本分析 (Cost Analysis)

#### 启动分析
- **URL**: `/analyze`
- **Method**: `POST`
- **Body**:
```json
{
  "drug_name": "string",
  "unit": "string",
  "costs": {
    "raw_material_cost": 0,
    "rd_cost": 0,
    "production_cost": 0,
    "equipment_cost": 0,
    "vehicle_cost": 0,
    "fuel_cost": 0,
    "inventory_loss_cost": 0,
    "warehouse_rent": 0,
    "energy_cost": 0,
    "custom_costs": [
      {
        "name": "string",
        "value": 0,
        "category": "string"
      }
    ]
  }
}
```
- **Response**:
```json
{
  "session_id": "string",
  "status": "started",
  "message": "string"
}
```

#### 获取分析状态与结果
- **URL**: `/status/{session_id}`
- **Method**: `GET`
- **Response**:
```json
{
  "session_id": "string",
  "status": "completed | started",
  "report": {
    "cost_summary": "string",
    "pricing_strategy": "string",
    "supply_chain_advice": "string"
  }
}
```

### 2.3 报告下载 (Reports)

#### 下载 PDF
- **URL**: `/reports/{session_id}/pdf`
- **Method**: `GET`
- **Response**: `application/pdf` 文件流

#### 下载 Word
- **URL**: `/reports/{session_id}/docx`
- **Method**: `GET`
- **Response**: `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 文件流
