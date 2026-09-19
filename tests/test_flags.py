import importlib
import os
import pytest

def test_hidayattube_flag_hard_fails(monkeypatch):
    monkeypatch.setenv("ENABLE_HIDAYATTUBE","true")
    with pytest.raises(RuntimeError):
        import core.config.flags as flags
        importlib.reload(flags)
    monkeypatch.delenv("ENABLE_HIDAYATTUBE",raising=False)
