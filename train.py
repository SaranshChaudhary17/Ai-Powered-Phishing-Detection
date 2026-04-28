import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from src.model_io import save_bundle
from src.url_features import build_feature_frame


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = PROJECT_ROOT / "data" / "phishing_site_urls.csv"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "phishing_url_model.joblib"
DEFAULT_METRICS_PATH = PROJECT_ROOT / "models" / "training_metrics.json"

LABEL_MAP = {"bad": 1, "good": 0}
DEFAULT_THRESHOLD = 0.65


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a phishing URL detector.")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="Path to the dataset CSV file.",
    )
    parser.add_argument(
        "--model-out",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Where to save the trained model.",
    )
    parser.add_argument(
        "--metrics-out",
        type=Path,
        default=DEFAULT_METRICS_PATH,
        help="Where to save training metrics as JSON.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Optional row limit for quicker experiments.",
    )
    return parser.parse_args()


def load_dataset(dataset_path: Path, sample_size: int | None) -> tuple[pd.Series, pd.Series]:
    df = pd.read_csv(dataset_path, usecols=["URL", "Label"])
    df = df.dropna(subset=["URL", "Label"]).copy()
    df["Label"] = df["Label"].str.lower().map(LABEL_MAP)
    df = df.dropna(subset=["Label"]).copy()
    df["Label"] = df["Label"].astype(int)

    if sample_size is not None:
        target_size = min(sample_size, len(df))
        fractions = df["Label"].value_counts(normalize=True)
        sampled_parts = []
        for label_value, fraction in fractions.items():
            label_df = df[df["Label"] == label_value]
            label_size = max(1, round(target_size * fraction))
            label_size = min(label_size, len(label_df))
            sampled_parts.append(label_df.sample(n=label_size, random_state=42))
        df = pd.concat(sampled_parts, ignore_index=True)

    return df["URL"].astype(str), df["Label"]


def main() -> None:
    args = parse_args()
    print(f"Loading dataset from {args.dataset} ...")
    urls, labels = load_dataset(args.dataset, args.sample_size)
    print(f"Rows loaded: {len(urls)}")

    print("Building expanded URL features ...")
    numeric_features = build_feature_frame(urls)
    feature_names = list(numeric_features.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        numeric_features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    print("Training model ...")
    model = RandomForestClassifier(
        n_estimators=320,
        max_depth=24,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X_train, y_train)

    print("Evaluating model ...")
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= DEFAULT_THRESHOLD).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "classification_report": classification_report(
            y_test,
            predictions,
            target_names=["good", "bad"],
            output_dict=True,
        ),
        "rows_used": int(len(urls)),
        "feature_names": feature_names,
        "default_threshold": DEFAULT_THRESHOLD,
        "model_family": "expanded_numeric_features_random_forest",
    }

    bundle = {
        "model": model,
        "feature_names": feature_names,
        "label_map": LABEL_MAP,
        "positive_label": "bad",
        "default_threshold": DEFAULT_THRESHOLD,
    }
    save_bundle(bundle, args.model_out)
    args.metrics_out.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Model saved to {args.model_out}")
    print(f"Metrics saved to {args.metrics_out}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"ROC AUC: {metrics['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
