"""Generate a copyright-safe procedural ambient tech bed for private review."""
from __future__ import annotations
import math, struct, wave
from pathlib import Path

RATE = 48000
SECONDS = 60
FREQS = (110.0, 164.81, 220.0, 329.63)

def main():
    out = Path("output/review/test1_v3_music.wav")
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        for n in range(RATE * SECONDS):
            t = n / RATE
            beat = math.sin(2*math.pi*1.5*t)
            pad = sum(math.sin(2*math.pi*f*t + 0.15*math.sin(t*0.4)) for f in FREQS) / len(FREQS)
            pulse = max(0.0, beat) * 0.08
            sample = max(-1.0, min(1.0, pad*0.055 + pulse))
            value = int(sample * 32767)
            w.writeframesraw(struct.pack("<hh", value, value))
    print(f"MUSIC READY: {out}")

if __name__ == "__main__":
    main()
