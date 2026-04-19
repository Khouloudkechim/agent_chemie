from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import analysis, simulate, stream, history, dataset
from core.config import settings

app = FastAPI(title="GazOptim AI", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(simulate.router, prefix="/api", tags=["Simulate"])
app.include_router(stream.router, prefix="/api", tags=["Stream"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(dataset.router, prefix="/api", tags=["Dataset"])

@app.get("/api/health")
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
