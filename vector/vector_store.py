import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseVectorStore(ABC):
    """向量存储基类"""
    
    @abstractmethod
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """添加文档到向量库"""
        pass

    @abstractmethod
    def query(self, query_text: str, n_results: int = 2) -> Dict[str, Any]:
        """查询向量库"""
        pass

class ChromaVectorStore(BaseVectorStore):
    def __init__(self, db_path: str, collection_name: str, model_path: str):
        self.db_path = db_path
        self.collection_name = collection_name
        self.model_path = model_path
        
        # 初始化 ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
        # 加载模型
        print(f"正在加载向量模型: {model_path} ...")
        self.model = SentenceTransformer(model_path)

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        if not documents:
            return
            
        embeddings = self.model.encode(documents).tolist()
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def clear_collection(self):
        """清空集合中的所有数据"""
        try:
            # 获取所有 ID
            existing_data = self.collection.get()
            ids = existing_data.get('ids', [])
            if ids:
                self.collection.delete(ids=ids)
                print(f"已清空集合 '{self.collection_name}'，共删除 {len(ids)} 条记录。")
            else:
                print(f"集合 '{self.collection_name}' 已经是空的。")
        except Exception as e:
            print(f"清空集合时出错: {e}")

    def ingest_from_jsonl(self, jsonl_path: str, batch_size: int = 100, clear_existing: bool = False):
        """从 JSONL 文件批量导入数据"""
        if not os.path.exists(jsonl_path):
            print(f"文件不存在: {jsonl_path}")
            return
            
        if clear_existing:
            self.clear_collection()

        print(f"开始从 {jsonl_path} 读取并入库...")
        
        ids = []
        texts = []
        metadatas = []
        total_added = 0
        
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    ids.append(data['id'])
                    
                    # 兼容 'text' 或 'content' 字段
                    text = data.get('text') or data.get('content')
                    if text is None:
                        print(f"跳过无内容行 (缺少 'text' 或 'content'): {line[:50]}...")
                        continue
                        
                    texts.append(text)
                    
                    # 构造元数据，保留除 id 和 content/text 之外的字段
                    metadata = data.get('metadata', {})
                    if not metadata:
                        # 如果没有 metadata 字段，则把其他字段放入 metadata
                        metadata = {k: v for k, v in data.items() if k not in ['id', 'text', 'content']}
                    
                    metadatas.append(metadata)
                    
                    if len(ids) >= batch_size:
                        self.add_documents(texts, metadatas, ids)
                        total_added += len(ids)
                        print(f"已入库 {total_added} 条...")
                        ids, texts, metadatas = [], [], []
                except json.JSONDecodeError:
                    print(f"跳过无效 JSON 行: {line[:50]}...")
                    continue
        
        # 处理剩余数据
        if ids:
            self.add_documents(texts, metadatas, ids)
            total_added += len(ids)
            
        print(f"✅ 所有数据入库完成！共 {total_added} 条。")

    def query(self, query_text: str, n_results: int = 2) -> Dict[str, Any]:
        q_emb = self.model.encode([query_text]).tolist()
        results = self.collection.query(query_embeddings=q_emb, n_results=n_results)
        return results
