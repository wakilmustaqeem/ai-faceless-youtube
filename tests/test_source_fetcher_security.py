from governance.source_fetcher import _public_http_url

def test_source_url_rejects_private_and_local_hosts():
    assert _public_http_url("http://127.0.0.1/") is False
    assert _public_http_url("http://localhost/") is False
    assert _public_http_url("http://192.168.1.10/") is False

def test_source_url_rejects_credentials_and_non_http():
    assert _public_http_url("http://user:pass@example.com/") is False
    assert _public_http_url("file:///etc/passwd") is False