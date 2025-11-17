from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from openai import OpenAI
import os
from dotenv import load_dotenv

# โหลด API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# สร้าง Qdrant local database
qdrant = QdrantClient(path="./qdrant")
COLLECTION = "docs"

print("vector_db.py ถูกโหลดแล้ว")  # debug

# สร้าง collection ใหม่
def init_db():
    try:
        qdrant.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        print("สร้าง collection เสร็จแล้ว")
    except Exception as e:
        print("init_db error:", e)

# แปลงข้อความเป็น embedding
def embed_text(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

# เพิ่ม document ลง database
def add_document(text, doc_id):
    vector = embed_text(text)
    try:
        qdrant.upsert(
            collection_name=COLLECTION,
            points=[{
                "id": doc_id,
                "vector": vector,
                "payload": {"text": text}
            }]
        )
        print(f"เพิ่ม doc {doc_id}: {text}")
    except Exception as e:
        print("add_document error:", e)

# ค้นหาจาก database
def search(query):
    qvec = embed_text(query)
    result = qdrant.search(
        collection_name=COLLECTION,
        query_vector=qvec,
        limit=3
    )
    return [hit.payload["text"] for hit in result]
