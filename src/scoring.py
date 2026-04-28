from pathlib import Path

import pandas as pd
from scipy.sparse import hstack

from src.model_io import load_bundle
from src.url_features import build_feature_frame


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "phishing_url_model.joblib"
DEFAULT_THRESHOLD = 0.80


def build_model_input(url: str, bundle: dict):
    numeric_frame = build_feature_frame(pd.Series([url], dtype="string"))
    numeric_frame = numeric_frame.reindex(columns=bundle["feature_names"])

    vectorizer = bundle.get("vectorizer")
    if vectorizer is None:
        return numeric_frame, numeric_frame

    text_matrix = vectorizer.transform([url])
    combined = hstack([text_matrix, numeric_frame.values])
    return combined, numeric_frame


def score_url(url: str, model_path: Path = DEFAULT_MODEL_PATH, threshold: float | None = None) -> dict:
    bundle = load_bundle(model_path)
    model = bundle["model"]
    default_threshold = DEFAULT_THRESHOLD
    threshold = default_threshold if threshold is None else float(threshold)

    model_input, numeric_frame = build_model_input(url, bundle)
    probability_bad = float(model.predict_proba(model_input)[0, 1])
    probability_good = 1.0 - probability_bad
    prediction = "bad" if probability_bad >= threshold else "good"

    return {
        "url": url,
        "prediction": prediction,
        "threshold": threshold,
        "probability_bad": probability_bad,
        "probability_good": probability_good,
        "risk_percent": round(probability_bad * 100, 2),
        "confidence_percent": round(max(probability_bad, probability_good) * 100, 2),
        "features": numeric_frame.iloc[0].to_dict(),
    }
