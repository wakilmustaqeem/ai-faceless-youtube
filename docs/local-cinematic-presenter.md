# Local Cinematic Presenter Pipeline v1

A free-first local assembly path using a supplied presenter asset, local TTS, optional 72-inch LCD artwork, and FFmpeg. Existing artifacts are never overwritten. A realistic presenter is an input asset unless a local generative model is installed; FFmpeg does not generate a human.

Example:
python scripts/local_presenter_pipeline.py --presenter assets/presenter.png --voice output/voice.mp3 --lcd assets/letust-gadget-lcd.png --output output/local-presenter-review.mp4

Public YouTube publishing remains OFF and human review remains required.
