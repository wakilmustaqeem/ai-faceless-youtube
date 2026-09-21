"""Free, deterministic source fetching with basic SSRF and redirect hardening."""
from __future__ import annotations

import hashlib
import ipaddress
import re
import socket
from html import unescape
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

MAX_BYTES = 2_000_000
TIMEOUT_SECONDS = 10
MAX_REDIRECTS = 3
ALLOWED_CONTENT_TYPES = ("text/html", "text/plain", "application/json", "application/xml", "text/xml")

class _LimitedRedirectHandler(HTTPRedirectHandler):
    max_redirections = MAX_REDIRECTS

def _public_ip(hostname: str) -> bool:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except OSError:
        return False
    addresses = {info[4][0] for info in infos}
    if not addresses:
        return False
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            return False
    return True

def _public_http_url(url: str) -> bool:
    p = urlparse(url.strip())
    return p.scheme in {"http", "https"} and bool(p.netloc) and not p.username and not p.password and _public_ip(p.hostname or "")

def _normalize(text: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text).strip()

def fetch_source(url: str) -> dict:
    if not _public_http_url(url):
        return {"passed": False, "reason": "invalid_or_private_source_url", "url": url}
    try:
        opener = build_opener(_LimitedRedirectHandler)
        req = Request(url, headers={"User-Agent": "AI-IT-Future-Tech-Research/1.0"})
        with opener.open(req, timeout=TIMEOUT_SECONDS) as response:
            final_url = response.geturl()
            if not _public_http_url(final_url):
                return {"passed": False, "reason": "unsafe_redirect_target", "url": final_url}
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                return {"passed": False, "reason": "source_too_large", "url": final_url}
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            return {"passed": False, "reason": "unsupported_content_type", "url": final_url, "content_type": content_type}
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