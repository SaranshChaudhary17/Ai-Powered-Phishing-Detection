from pathlib import Path

import joblib


def save_bundle(bundle: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, output_path)


def load_bundle(model_path: Path) -> dict:
    return joblib.load(model_path)
