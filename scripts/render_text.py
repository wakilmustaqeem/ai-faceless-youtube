"""Render English overlays through Chromium."""
from pathlib import Path
from html import escape
import asyncio
import sys
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "video_text.html"
CTA_TEMPLATE = ROOT / "cta_only.html"

async def _render_template(template_path: Path, replacements: dict[str, str], output_png: str) -> None:
    template = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace(key, escape(value))
    temp_html = ROOT / "output" / "_video_text_runtime.html"
    temp_html.parent.mkdir(parents=True, exist_ok=True)
    temp_html.write_text(template, encoding="utf-8")
    out = Path(output_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--font-render-hinting=none"])
        page = await browser.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
        await page.goto(temp_html.as_uri(), wait_until="load")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(300)
        if not await page.evaluate("document.fonts.check('52px Arial')"):
            raise RuntimeError("English overlay font did not load in Chromium")
        await page.screenshot(path=str(out), omit_background=True, full_page=False)
        await browser.close()

async def render(title: str, body: str, footer: str, output_png: str) -> None:
    await _render_template(TEMPLATE, {"__TITLE__":title,"__BODY__":body,"__FOOTER__":footer}, output_png)

async def render_cta(output_png: str) -> None:
    await _render_template(CTA_TEMPLATE, {}, output_png)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        asyncio.run(render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    elif len(sys.argv) == 3 and sys.argv[1] == "--cta":
        asyncio.run(render_cta(sys.argv[2]))
    else:
        raise SystemExit("Usage: render_text.py TITLE BODY FOOTER OUTPUT_PNG | --cta OUTPUT_PNG")
