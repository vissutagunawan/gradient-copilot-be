from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gradient Copilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict]] = []

class MaterialRecommendation(BaseModel):
    title: str
    url: str
    description: str
    source: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Gradient Copilot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gradient Copilot API"}

def get_fallback_materials(query: str) -> List[MaterialRecommendation]:
    """Fallback dummy materials when SerpAPI fails"""
    fallback_materials = [
        MaterialRecommendation(
            title=f"Panduan Lengkap {query.title()}",
            url="https://example.com/panduan-lengkap",
            description=f"Materi pembelajaran komprehensif tentang {query} dengan penjelasan step-by-step",
            source="example.com"
        ),
        MaterialRecommendation(
            title=f"Tutorial {query.title()} untuk Pemula",
            url="https://example.com/tutorial-pemula",
            description=f"Tutorial dasar {query} yang mudah dipahami untuk pemula",
            source="example.com"
        ),
        MaterialRecommendation(
            title=f"Video Course: Mastering {query.title()}",
            url="https://example.com/video-course",
            description=f"Kursus video lengkap tentang {query} dari dasar hingga mahir",
            source="example.com"
        )
    ]
    return fallback_materials

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)