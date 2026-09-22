# Local Graphic Studio

Offline/free-first PIL graphic tool for the cinematic presenter pipeline.

## Modes

`lcd` — Letust Gadget 72-inch LCD artwork  
`room` — cinematic room/background plate  
`title` — title card  
`lower-third` — presenter/name graphic  
`thumbnail` — enhance a local source image into a YouTube-style thumbnail

Existing output files are never overwritten.

## Examples

```bash
python scripts/local_graphic_studio.py lcd --output assets/letust-gadget-lcd-v2.png
python scripts/local_graphic_studio.py room --output assets/cinematic-room-bg-v2.png
python scripts/local_graphic_studio.py title --title "THE FUTURE OF AI" --output assets/title-card-v1.png
python scripts/local_graphic_studio.py lower-third --name "LETUST GADGET" --role "AI & IT FUTURE TECH" --output assets/lower-third-v1.png
python scripts/local_graphic_studio.py thumbnail --source assets/presenter.png --title "AI IN 2040" --output assets/thumbnail-v1.jpg
```

No network, API key, upload, or human-presenter generation is used.
