"""Local-first English master translation using Argos Translate.

Input JSON:
{"title": "...", "script": "...", "protected_terms": ["AI & IT Future Tech", ...]}

Output preserves protected terms and writes one locale JSON per requested target.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

LOCALES = ("ur", "ar", "hi", "es", "fr")

def _load_argos():
    try:
        import argostranslate.package
        import argostranslate.translate
    except ImportError as exc:
        raise RuntimeError("Argos Translate is not installed") from exc
    return argostranslate.package, argostranslate.translate

def ensure_language_pair(from_code: str, to_code: str, auto_install: bool) -> None:
    package, translate = _load_argos()
    installed = {lang.code for lang in translate.get_installed_languages()}
    if from_code in installed and to_code in installed:
        return
    if not auto_install:
        raise RuntimeError(f"Argos language pair {from_code}->{to_code} is not installed")
    package.update_package_index()
    candidates = [
        p for p in package.get_available_packages()
        if p.from_code == from_code and p.to_code == to_code
    ]
    if not candidates:
        raise RuntimeError(f"No Argos package available for {from_code}->{to_code}")
    package.install_from_path(candidates[0].download())

def _protect(text: str, terms: list[str]) -> tuple[str, dict[str, str]]:
    replacements = {}
    protected = text
    for i, term in enumerate(sorted(set(t for t in terms if t), key=len, reverse=True)):
        token = f"__PROTECTED_{i}__"
        protected = protected.replace(term, token)
        replacements[token] = term
    return protected, replacements

def _restore(text: str, replacements: dict[str, str]) -> str:
    for token, term in replacements.items():
        text = text.replace(token, term)
    return text

def translate_text(text: str, from_code: str, to_code: str, protected_terms: list[str]) -> str:
    package, translate = _load_argos()
    protected_text, replacements = _protect(text, protected_terms)
    installed = translate.get_installed_languages()
    source = next((x for x in installed if x.code == from_code), None)
    target = next((x for x in installed if x.code == to_code), None)
    if not source or not target:
        raise RuntimeError(f"Argos languages not installed: {from_code}, {to_code}")
    translation = source.get_translation(target)
    return _restore(translation.translate(protected_text), replacements)

def translate_package(data: dict, locale: str, auto_install: bool = False) -> dict:
    if locale not in LOCALES:
        raise ValueError(f"Unsupported phase-one locale: {locale}")
    protected = data.get("protected_terms", ["AI & IT Future Tech"])
    ensure_language_pair("en", locale, auto_install)
    return {
        "locale": locale,
        "source_locale": "en",
        "brand_name": "AI & IT Future Tech",
        "title": translate_text(data["title"], "en", locale, protected),
        "script": translate_text(data["script"], "en", locale, protected),
        "protected_terms": protected,
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--locales", nargs="+", default=list(LOCALES))
    parser.add_argument("--auto-install", action="store_true")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    for locale in args.locales:
        result = translate_package(data, locale, args.auto_install)
        (out / f"{locale}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Translated English master -> {locale}: {out / f'{locale}.json'}")

if __name__ == "__main__":
    main()
