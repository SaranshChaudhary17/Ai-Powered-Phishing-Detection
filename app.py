import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.scoring import score_url

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "web"

app = FastAPI(title="PhishGuard API")

# Enable CORS for all domains so the GitHub Pages frontend can connect to it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PredictRequest(BaseModel):
    url: str
    threshold: float = 0.80

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/example")
def get_example():
    example = (
        "http://login-verify-secure.accounts.com@45.23.10.198/"
        "webscr?cmd=update-billing-info-session-id-98327498"
    )
    return score_url(example)

@app.post("/api/predict")
def predict(request: PredictRequest):
    if not request.url.strip():
        raise HTTPException(status_code=400, detail="URL is required.")
    
    try:
        result = score_url(request.url.strip(), threshold=request.threshold)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/")
def serve_index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(index_path)

# Serve the rest of the static files (css, js)
app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    host = "0.0.0.0"
    # Hugging Face Spaces defaults to port 7860
    port = int(os.environ.get("PORT", 7860))
    print(f"Serving FastAPI app at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
