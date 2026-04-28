import argparse
from pathlib import Path

import pandas as pd

from src.model_io import load_bundle
from src.url_features import build_feature_frame


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = PROJECT_ROOT / "data" / "phishing_site_urls.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "phishing_url_model.joblib"
DEFAULT_THRESHOLD = 0.9


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append a confidently scored URL to the dataset.")
    parser.add_argument("--url", required=True, help="URL to score and potentially append.")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="Dataset CSV to update.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Trained model bundle path.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Minimum confidence required before appending.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.dataset)

    if args.url in df["URL"].astype(str).values:
        print("URL already exists in the dataset. No update made.")
        return

    bundle = load_bundle(args.model)
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    frame = build_feature_frame(pd.Series([args.url], dtype="string"))
    frame = frame.reindex(columns=feature_names)
    probability_bad = model.predict_proba(frame)[0, 1]
    probability_good = 1.0 - probability_bad
    confidence = max(probability_bad, probability_good)

    if confidence < args.threshold:
        print(f"Prediction confidence {confidence:.4f} is below {args.threshold:.2f}. No update made.")
        return

    label = "bad" if probability_bad >= 0.5 else "good"
    new_row = pd.DataFrame([{"URL": args.url, "Label": label}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(args.dataset, index=False)

    print(f"Added URL with label '{label}' and confidence {confidence:.4f}.")


if __name__ == "__main__":
    main()
