import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

# Model with 3 labels: "negative", "neutral", "positive"
# https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

_tokenizer = None
_model = None
_pipeline = None

def get_pipeline() -> TextClassificationPipeline:
    global _tokenizer, _model, _pipeline
    if _pipeline is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        _pipeline = TextClassificationPipeline(
            model=_model,
            tokenizer=_tokenizer,
            return_all_scores=True,
            top_k=None,
            function_to_apply="softmax",
            truncation=True
        )
    return _pipeline

def analyze_text(text: str):
    pipe = get_pipeline()
    t0 = time.time()
    scores = pipe(text)[0]  # list of dicts: [{"label": "...", "score": float}, ...]
    latency = (time.time() - t0) * 1000.0

    # Choose max-score label
    best = max(scores, key=lambda x: x["score"])
    # Normalize label capitalization to Title case
    best_label = best["label"].capitalize()

    # Convert to pydantic-friendly list
    out_scores = [{"label": s["label"].capitalize(), "score": float(s["score"])} for s in scores]
    return best_label, out_scores, latency