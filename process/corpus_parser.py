import os
import json
import fitz  # PyMuPDF
from docx import Document
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class BaseParser(ABC):
    """文件解析器基类"""
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """解析文件并返回文本内容"""
        pass

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> str:
        try:
            doc = fitz.open(file_path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        except Exception as e:
            print(f"解析 PDF 失败 {file_path}: {e}")
            return None

class DocxParser(BaseParser):
    def parse(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            print(f"解析 DOCX 失败 {file_path}: {e}")
            return None

class HTMLParser(BaseParser):
    def parse(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return BeautifulSoup(f, 'html.parser').get_text(separator=' ', strip=True)
        except Exception as e:
            print(f"解析 HTML 失败 {file_path}: {e}")
            return None

class TextParser(BaseParser):
    def parse(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"解析文本文件失败 {file_path}: {e}")
            return None

class CorpusProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.parsers = {
            '.pdf': PDFParser(),
            '.docx': DocxParser(),
            '.html': HTMLParser(),
            '.htm': HTMLParser(),
            '.txt': TextParser(),
            '.md': TextParser()
        }

    def register_parser(self, ext: str, parser: BaseParser):
        """注册自定义解析器"""
        self.parsers[ext.lower()] = parser

    def extract_text(self, file_path: str) -> str:
        """根据扩展名提取文本"""
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext)
        if parser:
            return parser.parse(file_path)
        else:
            print(f"未找到支持的解析器: {ext}")
            return None

    def chunk_text(self, text: str, source_name: str, med_name: str = ""):
        """将文本分块"""
        chunks = []
        start = 0
        length = len(text)
        # 如果文本为空，直接返回空列表
        if length == 0:
            return chunks
            
        while start < length:
            end = start + self.chunk_size
            segment = text[start:end]
            if segment.strip():
                chunks.append({
                    "id": f"{os.path.basename(source_name)}_{start}",
                    "text": segment,
                    "metadata": {"med_name": med_name, "source": source_name, "start": start}
                })
            start += (self.chunk_size - self.chunk_overlap)
        return chunks

    def process_to_jsonl(self, file_list: list, output_path: str, med_name: str = ""):
        """处理文件列表并保存为 JSONL"""
        print(f"开始解析 {len(file_list)} 个文件并保存为 {output_path} ...")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total_chunks = 0
        with open(output_path, 'w', encoding='utf-8') as f_out:
            for file_path in file_list:
                if not os.path.exists(file_path):
                    print(f"文件不存在: {file_path}")
                    continue
                    
                raw_text = self.extract_text(file_path)
                if not raw_text:
                    continue
                
                chunks = self.chunk_text(raw_text, file_path, med_name)
                
                for chunk in chunks:
                    f_out.write(json.dumps(chunk, ensure_ascii=False) + '\n')
                    total_chunks += 1
                
                print(f"已处理: {file_path} -> {len(chunks)} 个片段")
                
        print(f"✅ JSONL 生成完毕！共 {total_chunks} 条数据存储在 {output_path}")
