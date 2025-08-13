from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import AnalyzeRequest, AnalyzeResponse, BatchRequest, BatchResponse, BatchResponseItem, Score
from app.inference import analyze_text, MODEL_NAME

app = FastAPI(
    title="Sentiment API",
    version="1.0.0",
    description="3-class sentiment (Positive/Neutral/Negative) using a Hugging Face model."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    label, scores, latency = analyze_text(req.text)
    return {
        "label": label,
        "scores": scores,
        "model": MODEL_NAME,
        "latency_ms": latency
    }

@app.post("/batch", response_model=BatchResponse)
def batch(req: BatchRequest):
    results = []
    for item in req.items:
        label, scores, _ = analyze_text(item.text)
        results.append(BatchResponseItem(id=item.id, label=label, scores=[Score(**s) for s in scores]))
    return {"model": MODEL_NAME, "results": results}