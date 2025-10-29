# nlp.py
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import hashlib
import os
from mongoconnection import collection, save_analysis_results

# choose model - cardiffnlp or distilbert - adjust to availability
HF_MODEL = os.getenv("HF_MODEL", "cardiffnlp/twitter-roberta-base-sentiment")
MODEL_VERSION = "1.0"  # bump when you change modeling logic

# load transformers pipeline (lazy)
try:
    transformer_pipeline = pipeline("sentiment-analysis", model=HF_MODEL, top_k=None)
except Exception as e:
    transformer_pipeline = None
    print("Transformer pipeline failed to load:", e)

vader = SentimentIntensityAnalyzer()

def _text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def analyze_text(text, doc_id=None, force=False):
    """
    Check if text is already analyzed with same model_version.
    If not, run transformer if available, else VADER.
    Save back to Mongo with analysis_meta.
    Returns: dict {label, score, model, model_version, timestamp}
    """
    # check cache in mongo if doc_id provided
    if doc_id and not force:
        doc = collection.find_one({"_id": doc_id}, {"analysis_meta":1})
        if doc and doc.get("analysis_meta") and doc["analysis_meta"].get("model_version") == MODEL_VERSION:
            return doc["analysis_meta"]

    # Run transformer if available
    try:
        if transformer_pipeline:
            res = transformer_pipeline(text if text else "")[0]
            # label mapping depends on model; adapt if needed
            label = res.get("label")
            score = float(res.get("score", 0.0))
            if "LABEL" in label:
                # heuristic: map labels to Pos/Neg/Neutral if necessary
                if label.endswith("0"):
                    canonical = "Negative"
                elif label.endswith("1"):
                    canonical = "Neutral"
                else:
                    canonical = "Positive"
            else:
                # many HF sentiment models return POS/NEG
                canonical = "Positive" if "POS" in label.upper() or "POSITIVE" in label.upper() else \
                            "Negative" if "NEG" in label.upper() or "NEGATIVE" in label.upper() else "Neutral"
            meta = {
                "label": canonical,
                "raw_label": label,
                "score": score,
                "model": HF_MODEL,
                "model_version": MODEL_VERSION,
                "analyzed_at": datetime.utcnow()
            }
        else:
            raise RuntimeError("Transformer pipeline not available")
    except Exception:
        # fallback to VADER
        vs = vader.polarity_scores(text)
        compound = vs["compound"]
        canonical = "Positive" if compound > 0.05 else "Negative" if compound < -0.05 else "Neutral"
        meta = {
            "label": canonical,
            "raw_scores": vs,
            "model": "vader",
            "model_version": "vader-1.0",
            "analyzed_at": datetime.utcnow()
        }

    # Write back to mongo if doc_id provided
    if doc_id:
        save_analysis_results(doc_id, meta["label"], meta)

    return meta
