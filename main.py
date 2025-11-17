from fastapi import FastAPI
from pydantic import BaseModel
from vector_db import search
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question

    # ค้นหาข้อมูลใกล้เคียงจาก database
    docs = search(question)
    context = "\n".join(docs)

    # ส่งเข้า AI เพื่อ generate ตอบ
    prompt = f"ใช้ข้อมูลต่อไปนี้ตอบคำถามของผู้ใช้:\n{context}\n\nคำถาม: {question}\nตอบ:"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return {"answer": answer}
