import os
import sys

# Add project root to path so we can import backend modules easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from backend.benchmarking.metrics import Benchmarker

app = FastAPI(title="Emergency Dispatch System API")

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
os.makedirs(frontend_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class BenchmarkRequest(BaseModel):
    sizes: List[int]
    distribution: str

@app.get("/")
def read_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.post("/benchmark")
def run_benchmark(req: BenchmarkRequest):
    results = Benchmarker.run_all_benchmarks(req.sizes, req.distribution)
    return {"status": "success", "data": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
