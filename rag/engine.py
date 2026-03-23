import os
import sys
from typing import List, Dict, Any

# Ensure we can import from vector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vector.vector_store import ChromaVectorStore
from .llm_client import BaseLLM

# Default Prompt Template
RAG_PROMPT_TEMPLATE = """
根据上下文回答用户问题，标明内容对应的来源。

Context:
{context_str}

User Question: {query}

Answer:
"""

class DrugRAGSystem:
    def __init__(self, drug_name: str, jsonl_path: str, db_base_path: str, model_path: str, llm: BaseLLM, prompt_template: str = RAG_PROMPT_TEMPLATE):
        self.drug_name = drug_name
        self.jsonl_path = jsonl_path
        self.db_path = os.path.join(db_base_path, drug_name)
        self.model_path = model_path
        self.llm = llm
        self.prompt_template = prompt_template
        
        # Initialize Vector Store
        # Collection name can be sanitized drug name
        collection_name = "drug_kb"
        self.vector_store = ChromaVectorStore(
            db_path=self.db_path,
            collection_name=collection_name,
            model_path=model_path
        )

    def build_knowledge_base(self):
        """Builds or updates the vector database from JSONL."""
        print(f"Building Knowledge Base for '{self.drug_name}'...")
        if not os.path.exists(self.jsonl_path):
            print(f"Error: JSONL file not found at {self.jsonl_path}")
            return
            
        self.vector_store.ingest_from_jsonl(self.jsonl_path)
        print(f"Knowledge Base for '{self.drug_name}' is ready at {self.db_path}")

    def query_knowledge(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Queries the vector store for relevant documents."""
        results = self.vector_store.query(query, n_results=top_k)
        return results

    def answer_question(self, query: str, top_k: int = 3) -> str:
        """Retrieves context and generates an answer using LLM."""
        # 1. Retrieve
        search_results = self.query_knowledge(query, top_k=top_k)
        
        # Extract documents
        documents = search_results.get('documents', [[]])[0]
        metadatas = search_results.get('metadatas', [[]])[0]
        
        if not documents:
            return "Sorry, I couldn't find any relevant information in the knowledge base."
            
        # 2. Format Context
        context_parts = []
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            source = meta.get('source', 'Unknown')
            context_parts.append(f"Source {i+1} ({source}):\n{doc}")
            
        context_str = "\n\n".join(context_parts)
        
        # 3. Generate Answer
        prompt = self.prompt_template.format(context_str=context_str, query=query)

        # Call LLM
        # Note: We pass context=[] because we have already formatted the context into the prompt string.
        # This prevents the LLM client from double-injecting the context.
        response = self.llm.generate(prompt, context=[])
        
        return response
