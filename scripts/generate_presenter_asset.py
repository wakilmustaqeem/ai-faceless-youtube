"""Generate the Premium Tech v3 presenter/LCD visual anchor.

The production pipeline uses one consistent full-body presenter asset across all
scenes. A checked-in asset is intentionally avoided; CI can generate it from the
configured free/open image provider, while a local file can be supplied for manual
production/review.
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import os

from PIL import Image

W, H = 1080, 1920
OUT = Path("output/presenter_anchor.png")

PROMPT = (
    "photorealistic full-body adult male technology presenter, standing naturally "
    "in a premium dark cinematic technology studio, visible head to shoes, natural "
    "human proportions and realistic skin, confident calm expression, modern smart "
    "casual clothing, practical key light and subtle cool rim light, a large 72-inch "
    "LCD display clearly visible behind him showing abstract consumer gadget UI and "
    "a generic smartwatch/product dashboard, restrained glass HUD accents around the "
    "screen, clean charcoal and black studio, cyan and white interface highlights, "
    "cinematic depth of field, realistic photography, no celebrity likeness, no "
    "brand logos, no text, no watermark, portrait 9:16 composition, presenter "
    "centered with safe negative space around face and body"
)

def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "ai-faceless-youtube/1.0"})
    with urlopen(request, timeout=120) as response:
        data = response.read()
    if not data:
        raise RuntimeError("Image provider returned an empty response")
    destination.write_bytes(data)

def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    local = os.getenv("PRESENTER_ASSET")
    if local:
        source = Path(local)
        if not source.exists():
            raise FileNotFoundError(f"PRESENTER_ASSET does not exist: {source}")
        Image.open(source).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(OUT)
    else:
        endpoint = os.getenv(
            "POLLINATIONS_IMAGE_ENDPOINT",
            "https://image.pollinations.ai/prompt",
        )
        model = os.getenv("POLLINATIONS_IMAGE_MODEL", "flux")
        url = (
            f"{endpoint.rstrip('/')}/{quote(PROMPT, safe='')}"
            f"?model={quote(model)}&width={W}&height={H}&nologo=true"
        )
        download(url, OUT)

    with Image.open(OUT) as image:
        if image.width < 720 or image.height < 1280:
            raise RuntimeError(
                f"Presenter asset is too small: {image.width}x{image.height}; "
                "expected at least 720x1280"
            )
        image.convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(OUT)

    print(f"Verified presenter anchor: {OUT} ({W}x{H})")

if __name__ == "__main__":
    main()
