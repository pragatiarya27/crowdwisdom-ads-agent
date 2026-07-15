import os
import json
import chromadb
from hermes.skill import BaseSkill
from config import CHROMA_DB_DIR, PDF_DATA_DIR

class RAGSkill(BaseSkill):
    name = "rag_skill"

    def __init__(self):
        print("🔧 [RAG] Setting up ChromaDB...")
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection("crowdwisdom")
        print("✅ [RAG] Ready!")

    def get_embedding(self, text: str) -> list:
        # simple hash-based embedding (no torch needed)
        import hashlib
        hash_val = hashlib.md5(text.encode()).hexdigest()
        vec = []
        for i in range(0, min(len(hash_val), 48), 2):
            vec.append(int(hash_val[i:i+2], 16) / 255.0)
        while len(vec) < 384:
            vec.append(0.0)
        return vec[:384]

    def load_json_files(self):
        # reads both JSON data files and extracts text chunks
        chunks = []
        json_files = [
            os.path.join(PDF_DATA_DIR, "crowdwisdom_data_1.json"),
            os.path.join(PDF_DATA_DIR, "crowdwisdom_data_2.json")
        ]
        for json_path in json_files:
            if not os.path.exists(json_path):
                print(f"⚠️  [RAG] File not found: {json_path}")
                continue
            print(f"📄 [RAG] Loading {json_path}...")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # extract all string values from JSON
            def extract_strings(obj, depth=0):
                if depth > 5:
                    return
                if isinstance(obj, str) and len(obj) > 50:
                    chunks.append(obj)
                elif isinstance(obj, dict):
                    for v in obj.values():
                        extract_strings(v, depth+1)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_strings(item, depth+1)
            extract_strings(data)
        print(f"✅ [RAG] Loaded {len(chunks)} chunks from data files")
        return chunks

    def index_pdfs(self):
        if self.collection.count() > 0:
            print(f"✅ [RAG] Already indexed {self.collection.count()} chunks")
            return
        chunks = self.load_json_files()
        if not chunks:
            print("⚠️  [RAG] No chunks to index!")
            return
        print(f"🔧 [RAG] Embedding {len(chunks)} chunks...")
        embeddings = [self.get_embedding(chunk) for chunk in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        self.collection.add(documents=chunks, embeddings=embeddings, ids=ids)
        print(f"✅ [RAG] Indexed {len(chunks)} chunks into ChromaDB!")

    def query(self, query_text: str, top_k: int = 3) -> list:
        if self.collection.count() == 0:
            return []
        query_embedding = self.get_embedding(query_text)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count())
        )
        return results["documents"][0] if results["documents"] else []

    def run(self, input: dict) -> dict:
        self.index_pdfs()
        query = input.get("query", "crowd wisdom trading unique data statistics")
        chunks = self.query(query)
        return {"query": query, "chunks": chunks}