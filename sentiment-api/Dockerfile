FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Pre-warm model weights at build (optional; can be done at runtime instead)
# Comment out if your host limits build-time downloads.
# RUN python - <<'PY'\nfrom transformers import AutoTokenizer, AutoModelForSequenceClassification\nm='cardiffnlp/twitter-roberta-base-sentiment-latest'\nAutoTokenizer.from_pretrained(m)\nAutoModelForSequenceClassification.from_pretrained(m)\nPY

COPY app ./app
COPY uvicorn.yaml ./uvicorn.yaml

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080", "--log-config=uvicorn.yaml"]