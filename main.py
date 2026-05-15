import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router

app = FastAPI(
    title="Alchemist's Crypt AI Hive Mind",
    description="Tactical AI Backend for Unity FPS",
    version="0.1.0"
)

# Enable CORS for Unity builds (WebGL or standalone)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hive Mind is operational. The Pharaoh awaits."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
