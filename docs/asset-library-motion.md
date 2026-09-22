# Asset Library + Auto Motion

The local production branch now has a safe asset-library manager.

## Asset library

Downloaded assets go to:

`assets/library/`

Only explicitly supplied direct public asset URLs are accepted. The downloader:
- refuses to overwrite an existing file
- records a SHA-256 digest
- accepts common image/video formats
- does not upload anything

Example:

```bash
python scripts/asset_library_motion.py download "<DIRECT_ASSET_URL>" --name future-city.jpg
```

A direct URL is required; the script does not scrape search-result pages.

## Motion presets

Available presets:

- `slow-zoom`
- `slow-push`
- `pan-left`
- `pan-right`
- `static`

Example:

```bash
python scripts/asset_library_motion.py motion slow-push
```

The returned FFmpeg filter can be inserted into the local cinematic compositor. Motion is deterministic and subtle rather than random, so the same source produces repeatable output.

Public publishing remains OFF and human review remains required.
