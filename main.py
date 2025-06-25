from fastapi import FastAPI
import requests
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

def extract_learning_keywords(message: str) -> str:
    """Extract learning-related keywords from user message"""
    learning_indicators = [
        "belajar", "materi", "tutorial", "course", "kursus", "pelajaran",
        "pembelajaran", "edukasi", "panduan", "guide", "cara", "how to",
        "explain", "jelaskan", "ajarkan", "teach", "study", "kuliah"
    ]
    
    message_lower = message.lower()

    has_learning_intent = any(indicator in message_lower for indicator in learning_indicators)
    
    if has_learning_intent:
        words = message.split()
        stop_words = {"saya", "aku", "untuk", "tentang", "yang", "dan", "atau", "adalah", "ini", "itu"}
        keywords = [word for word in words if len(word) > 3 and word.lower() not in stop_words]
        
        return " ".join(keywords[:3])  # Take first 3 meaningful words
    
    return ""

def search_learning_materials(query: str) -> List[MaterialRecommendation]:
    """Search for learning materials using SerpAPI"""
    try:
        search_query = f"{query} tutorial course learning material"
        
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": SERP_API_KEY,
            "num": 8,
            "hl": "id",
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()
        
        materials = []
        organic_results = results.get("organic_results", [])
        
        educational_domains = [
            "youtube.com", "coursera.org", "udemy.com", "khanacademy.org",
            "edx.org", "wikipedia.org", "medium.com", "github.com",
            "stackoverflow.com", "w3schools.com", "geeksforgeeks.org",
            "freecodecamp.org", "codecademy.com"
        ]
        
        for result in organic_results[:5]:
            title = result.get("title", "")
            url = result.get("link", "")
            snippet = result.get("snippet", "")
            
            is_educational = any(domain in url.lower() for domain in educational_domains)
            
            if title and url and (is_educational or "tutorial" in title.lower() or "course" in title.lower()):
                materials.append(MaterialRecommendation(
                    title=title,
                    url=url,
                    description=snippet[:150] + "..." if len(snippet) > 150 else snippet,
                    source=url.split('/')[2] if '/' in url else url
                ))
        
        return materials[:4]
        
    except Exception as e:
        print(f"SerpAPI error: {e}")
        return get_fallback_materials(query)

def create_learning_prompt(user_message: str, materials: List[MaterialRecommendation], conversation_history: List[Dict]) -> str:
    """Create a structured prompt for Gemini with learning materials"""
    
    context = ""
    if conversation_history:
        context = "\n".join([
            f"{'User' if msg.get('role') == 'user' else 'Assistant'}: {msg.get('content', '')}"
            for msg in conversation_history[-4:]  # Last 4 messages for context
        ])
        context = f"Conversation Context:\n{context}\n\n"
    
    materials_text = ""
    if materials:
        materials_text = "Materi Pembelajaran yang Relevan:\n"
        for i, material in enumerate(materials, 1):
            materials_text += f"{i}. {material.title}\n   URL: {material.url}\n   Deskripsi: {material.description}\n\n"
    
    prompt = f"""Kamu adalah Gradient Copilot, asisten pembelajaran AI yang membantu pengguna belajar berbagai topik.

{context}Pertanyaan User: {user_message}

{materials_text}

Instruksi:
1. Berikan jawaban yang helpful dan educational dalam bahasa Indonesia
2. Jika user menanyakan materi pembelajaran, reference materi yang sudah diberikan di atas
3. Berikan penjelasan yang clear dan easy to understand
4. Jika ada materi pembelajaran yang relevan, suggest user untuk mengunjungi link tersebut
5. Gunakan format yang rapi dengan bullet points atau numbering jika perlu
6. Sesuaikan tone dengan friendly dan encouraging

Jawab dengan format:
- Penjelasan/jawaban utama
- Rekomendasi materi (jika ada dan relevan)
- Tips tambahan (jika perlu)"""

    return prompt

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)