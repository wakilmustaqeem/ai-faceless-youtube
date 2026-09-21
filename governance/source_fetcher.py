"""Free, deterministic source fetching and provenance checks for claim evidence."""
from __future__ import annotations

import hashlib
import re
from html import unescape
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MAX_BYTES = 2_000_000
TIMEOUT_SECONDS = 10

def _public_http_url(url: str) -> bool:
    p = urlparse(url.strip())
    return p.scheme in {"http", "https"} and bool(p.netloc) and not p.username and not p.password

def _normalize(text: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text).strip()

def fetch_source(url: str) -> dict:
    if not _public_http_url(url):
        return {"passed": False, "reason": "invalid_source_url", "url": url}
    try:
        req = Request(url, headers={"User-Agent": "AI-IT-Future-Tech-Research/1.0"})
        with urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            data = response.read(MAX_BYTES + 1)
            final_url = response.geturl()
            if len(data) > MAX_BYTES:
                return {"passed": False, "reason": "source_too_large", "url": final_url}
            content_type = response.headers.get("Content-Type", "")
        text = _normalize(data.decode("utf-8", errors="replace"))
        if not text:
            return {"passed": False, "reason": "empty_source", "url": final_url}
        return {"passed": True, "url": final_url, "content_type": content_type, "text": text, "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    except Exception as exc:
        return {"passed": False, "reason": "source_fetch_failed", "error_type": type(exc).__name__, "url": url}

def verify_evidence_in_source(evidence: str, source_text: str) -> bool:
    evidence = _normalize(evidence)
    source_text = _normalize(source_text)
    if not evidence or not source_text:
        return False
    return evidence in source_text