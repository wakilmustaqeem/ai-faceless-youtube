"""Local-first English master translation using Argos Translate.

Input JSON:
{"title": "...", "script": "...", "protected_terms": ["AI & IT Future Tech", ...]}

Output preserves protected terms and writes one locale JSON per requested target.
"""
from __future__ import annotations
import argparse, json
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


def _translate_with_protected_terms(text: str, translation, protected_terms: list[str]) -> str:
    """Translate segments while never sending protected terms to Argos."""
    terms = sorted(set(term for term in protected_terms if term), key=len, reverse=True)
    if not terms:
        return translation.translate(text)

    parts: list[str] = []
    cursor = 0
    while cursor < len(text):
        matches = [
            (text.find(term, cursor), term)
            for term in terms
            if text.find(term, cursor) >= 0
        ]
        if not matches:
            parts.append(translation.translate(text[cursor:]))
            break

        start, term = min(matches, key=lambda item: item[0])
        if start > cursor:
            parts.append(translation.translate(text[cursor:start]))
        parts.append(term)
        cursor = start + len(term)

    return "".join(parts)


def translate_text(text: str, from_code: str, to_code: str, protected_terms: list[str]) -> str:
    _, translate = _load_argos()
    installed = translate.get_installed_languages()
    source = next((x for x in installed if x.code == from_code), None)
    target = next((x for x in installed if x.code == to_code), None)
    if not source or not target:
        raise RuntimeError(f"Argos languages not installed: {from_code}, {to_code}")
    translation = source.get_translation(target)
    return _translate_with_protected_terms(text, translation, protected_terms)


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
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    for locale in args.locales:
        result = translate_package(data, locale, args.auto_install)
        (out / f"{locale}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Translated English master -> {locale}: {out / f'{locale}.json'}")


if __name__ == "__main__":
    main()
