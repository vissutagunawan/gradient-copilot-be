from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Gradient Copilot API", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gradient Copilot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)