import argparse
from pathlib import Path

from src.scoring import score_url


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "phishing_url_model.joblib"
DEFAULT_THRESHOLD = 0.80
DEFAULT_URL = (
    "http://login-verify-secure.accounts.com@45.23.10.198/"
    "webscr?cmd=update-billing-info-session-id-98327498"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict whether a URL is phishing.")
    parser.add_argument("--url", type=str, default=DEFAULT_URL, help="URL to score.")
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path to the trained model bundle.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="Probability threshold for labeling a URL as phishing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = score_url(args.url, args.model, args.threshold)

    print(f"URL: {args.url}")
    print(f"Prediction: {result['prediction']}")
    print(f"Phishing probability: {result['probability_bad']:.4f}")
    print(f"Decision threshold: {result['threshold']:.2f}")
    print("Features:")
    for key, value in result["features"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
