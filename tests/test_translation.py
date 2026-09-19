import json
from pathlib import Path
import scripts.translate as translate

def test_phase_one_locales():
    assert set(translate.LOCALES) == {"ur", "ar", "hi", "es", "fr"}

def test_brand_is_protected(monkeypatch):
    monkeypatch.setattr(translate, "ensure_language_pair", lambda *args, **kwargs: None)
    class FakeTranslation:
        def translate(self, text):
            return text.replace("__PROTECTED_0__", "AI & IT Future Tech") + " translated"
    class FakeLang:
        code = "en"
        def get_translation(self, target):
            return FakeTranslation()
    class FakeTarget:
        code = "ur"
    monkeypatch.setattr(translate, "_load_argos", lambda: (None, type("T", (), {"get_installed_languages": staticmethod(lambda: [FakeLang(), FakeTarget()])})))
    data = json.loads(Path("tests/fixtures/translation_input.json").read_text(encoding="utf-8"))
    result = translate.translate_package(data, "ur")
    assert result["brand_name"] == "AI & IT Future Tech"
    assert "AI & IT Future Tech" in result["script"]
