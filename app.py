import json
import mimetypes
import os
import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from src.scoring import score_url


PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "web"
HOST = "127.0.0.1"
PORT = 8000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the phishing detection web server.")
    parser.add_argument("--host", default=HOST, help="Host to bind the server to.")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PHISHGUARD_PORT", PORT)),
        help="Port to bind the server to.",
    )
    return parser.parse_args()


class ModelServerHandler(BaseHTTPRequestHandler):
    server_version = "PhishGuard/1.0"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        if route == "/api/example":
            example = (
                "http://login-verify-secure.accounts.com@45.23.10.198/"
                "webscr?cmd=update-billing-info-session-id-98327498"
            )
            self._send_json(HTTPStatus.OK, score_url(example))
            return

        if route == "/":
            self._serve_file(STATIC_DIR / "index.html")
            return

        target = (STATIC_DIR / route.lstrip("/")).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.exists():
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return
        self._serve_file(target)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/predict":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body is required."})
            return

        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON body."})
            return

        url = str(payload.get("url", "")).strip()
        threshold = float(payload.get("threshold", 0.80))

        if not url:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "URL is required."})
            return

        try:
            result = score_url(url, threshold=threshold)
        except Exception as exc:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        self._send_json(HTTPStatus.OK, result)

    def log_message(self, format: str, *args) -> None:
        return

    def _serve_file(self, path: Path) -> None:
        content_type, _ = mimetypes.guess_type(path.name)
        if path.suffix == ".js" and content_type is None:
            content_type = "application/javascript"
        if path.suffix == ".css" and content_type is None:
            content_type = "text/css"
        if content_type is None:
            content_type = "text/html; charset=utf-8"

        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    args = parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), ModelServerHandler)
    print(f"Serving phishing detection app at http://{args.host}:{args.port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
