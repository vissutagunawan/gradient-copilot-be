from fastapi import FastAPI

app = FastAPI(title="Gradient Copilot API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gradient Copilot API"}