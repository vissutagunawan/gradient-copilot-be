from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = FastAPI(title="Gradient Copilot API", version="1.0.0")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gradient Copilot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gradient Copilot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)