import math
import re
from collections import Counter
from urllib.parse import parse_qs, urlparse

import pandas as pd


SUSPICIOUS_KEYWORDS = (
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "bank",
    "confirm",
    "password",
    "signin",
    "webscr",
    "billing",
    "payment",
)

BRANDS = (
    "google",
    "paypal",
    "facebook",
    "amazon",
    "apple",
    "microsoft",
    "instagram",
    "netflix",
    "linkedin",
)

IPV4_PATTERN = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def ensure_scheme(url: str) -> str:
    if "://" in url:
        return url
    return f"http://{url}"


def safe_urlparse(url: str):
    normalized = ensure_scheme(url)
    try:
        return urlparse(normalized)
    except ValueError:
        cleaned = normalized.replace("[", "%5B").replace("]", "%5D")
        return urlparse(cleaned)


def get_hostname(url: str) -> str:
    parsed = safe_urlparse(url)
    return (parsed.hostname or "").lower()


def get_registered_domain(hostname: str) -> str:
    parts = [part for part in hostname.split(".") if part]
    if len(parts) >= 2:
        return parts[-2]
    if parts:
        return parts[0]
    return ""


def subdomain_count(hostname: str) -> int:
    if IPV4_PATTERN.fullmatch(hostname):
        return 3

    parts = [part for part in hostname.split(".") if part]
    if len(parts) <= 2:
        return 0
    return len(parts) - 2


def url_entropy(url: str) -> float:
    counts = Counter(url)
    length = len(url) or 1
    probabilities = [count / length for count in counts.values()]
    return -sum(prob * math.log2(prob) for prob in probabilities)


def count_suspicious_keywords(text: str) -> int:
    lowered = text.lower()
    return sum(keyword in lowered for keyword in SUSPICIOUS_KEYWORDS)


def brand_misuse(url: str, hostname: str) -> int:
    registered_domain = get_registered_domain(hostname)
    lowered_url = url.lower()

    for brand in BRANDS:
        if brand in lowered_url and brand not in registered_domain:
            return 1
    return 0


def create_features(url: str) -> dict:
    parsed = safe_urlparse(url)
    hostname = get_hostname(url)
    path = parsed.path or ""
    query = parsed.query or ""
    params = parse_qs(query, keep_blank_values=True)
    host_parts = [part for part in hostname.split(".") if part]
    path_parts = [part for part in path.split("/") if part]
    url_tokens = [token for token in re.split(r"[^A-Za-z0-9]+", url.lower()) if token]
    avg_token_length = sum(len(token) for token in url_tokens) / len(url_tokens) if url_tokens else 0.0
    max_token_length = max((len(token) for token in url_tokens), default=0)
    query_keys = [key.lower() for key in params.keys()]
    suspicious_query_keys = {"login", "verify", "token", "session", "account", "password", "redirect", "update", "billing"}
    try:
        has_port = int(parsed.port is not None)
    except ValueError:
        has_port = 0

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "num_digits": sum(char.isdigit() for char in url),
        "num_special_chars": sum(not char.isalnum() for char in url),
        "has_at_symbol": int("@" in url),
        "uses_ip_address": int(bool(IPV4_PATTERN.search(hostname))),
        "subdomain_count": subdomain_count(hostname),
        "has_https": int(parsed.scheme.lower() == "https"),
        "url_entropy": url_entropy(url),
        "suspicious_keyword_hits": count_suspicious_keywords(url),
        "brand_misuse": brand_misuse(url, hostname),
        "has_port": has_port,
        "num_query_params": len(params),
        "has_fragment": int(bool(parsed.fragment)),
        "hostname_token_count": len(host_parts),
        "path_segment_count": len(path_parts),
        "avg_token_length": avg_token_length,
        "max_token_length": max_token_length,
        "has_www_prefix": int(hostname.startswith("www.")),
        "query_has_suspicious_key": int(any(key in suspicious_query_keys for key in query_keys)),
        "double_slash_path": int("//" in path),
        "path_has_file_extension": int(bool(re.search(r"\.[a-zA-Z0-9]{2,5}$", path))),
    }
    return features


def build_feature_frame(urls: pd.Series) -> pd.DataFrame:
    rows = [create_features(str(url)) for url in urls]
    return pd.DataFrame(rows)
