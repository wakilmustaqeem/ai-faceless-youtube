#!/usr/bin/env python3
"""AI & IT Future Tech — Cinematic Presenter Studio v2.

One local GUI for:
- full-body presenter asset intake/verification
- Edge-TTS or optional ElevenLabs narration
- local LCD/graphic assets
- FFmpeg cinematic assembly

No existing output is overwritten. Main branch is never touched by this tool.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "scripts" / "local_presenter_pipeline.py"
GRAPHICS = ROOT / "scripts" / "local_graphic_studio.py"
VOICE_EDGE = ROOT / "scripts" / "generate_voice.py"
VOICE_ELEVEN = ROOT / "scripts" / "elevenlabs_voice.py"
PRESENTER_VERIFY = ROOT / "scripts" / "presenter_asset_factory.py"


class Studio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI & IT Future Tech — Cinematic Presenter Studio v2")
        self.geometry("930x790")
        self.resizable(False, False)

        self.vars = {
            k: tk.StringVar()
            for k in (
                "presenter", "voice", "lcd", "background", "output",
                "voice_engine", "eleven_voice_id", "eleven_model", "motion"
            )
        }
        self.vars["output"].set(str(ROOT / "output" / "cinematic-presenter-review-v2.mp4"))
        self.vars["voice_engine"].set("Edge-TTS")
        self.vars["eleven_voice_id"].set("JBFqnCBsd6RMkjVDRZzb")
        self.vars["eleven_model"].set("eleven_multilingual_v2")
        self.vars["motion"].set("slow-push")

        self._build()

    def _row(self, label, key, types, r):
        ttk.Label(self, text=label).grid(row=r, column=0, sticky="w", padx=14, pady=6)
        ttk.Entry(self, textvariable=self.vars[key], width=67).grid(row=r, column=1, padx=8)
        ttk.Button(self, text="Browse", command=lambda: self._pick(key, types)).grid(row=r, column=2, padx=10)

    def _build(self):
        ttk.Label(
            self, text="Local Cinematic Presenter Studio v2",
            font=("TkDefaultFont", 17, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(16, 4))
        ttk.Label(
            self,
            text="Presenter verification + natural voice generation + LCD + FFmpeg • Main untouched"
        ).grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self._row(
            "Full-body realistic presenter asset", "presenter",
            [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 2
        )

        ttk.Label(self, text="Narration script").grid(
            row=3, column=0, sticky="nw", padx=14, pady=6
        )
        self.script = tk.Text(self, width=67, height=7, wrap="word")
        self.script.grid(row=3, column=1, padx=8, pady=6)
        self.script.insert(
            "1.0",
            "Welcome to AI and IT Future Tech. Today we are exploring how AI is changing the way we build, learn, and work."
        )

        ttk.Label(self, text="Voice engine").grid(row=4, column=0, sticky="w", padx=14, pady=6)
        ttk.Combobox(
            self, textvariable=self.vars["voice_engine"],
            values=("Edge-TTS", "ElevenLabs"), state="readonly", width=64
        ).grid(row=4, column=1, padx=8, sticky="w")

        ttk.Label(self, text="ElevenLabs voice ID").grid(row=5, column=0, sticky="w", padx=14, pady=6)
        ttk.Entry(self, textvariable=self.vars["eleven_voice_id"], width=67).grid(row=5, column=1, padx=8)

        ttk.Label(self, text="ElevenLabs model").grid(row=6, column=0, sticky="w", padx=14, pady=6)
        ttk.Entry(self, textvariable=self.vars["eleven_model"], width=67).grid(row=6, column=1, padx=8)

        self._row(
            "Generated natural voice", "voice",
            [("Audio", "*.mp3 *.wav *.m4a *.aac"), ("All files", "*.*")], 7
        )
        self._row(
            "72-inch LCD artwork", "lcd",
            [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 8
        )
        self._row(
            "Cinematic background", "background",
            [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 9
        )
        self._row(
            "New output file", "output",
            [("MP4", "*.mp4"), ("All files", "*.*")], 10
        )

        ttk.Label(self, text="Motion").grid(row=11, column=0, sticky="w", padx=14, pady=6)
        ttk.Combobox(
            self, textvariable=self.vars["motion"],
            values=("static", "slow-zoom", "slow-push", "pan-left", "pan-right"),
            state="readonly", width=64
        ).grid(row=11, column=1, padx=8, sticky="w")

        tools1 = ttk.Frame(self)
        tools1.grid(row=12, column=0, columnspan=3, pady=12)
        ttk.Button(tools1, text="VERIFY PRESENTER", command=self.verify_presenter).pack(side="left", padx=5)
        ttk.Button(tools1, text="GENERATE NATURAL VOICE", command=self.generate_voice).pack(side="left", padx=5)
        ttk.Button(tools1, text="OPEN GRAPHIC STUDIO", command=self.open_graphic_studio).pack(side="left", padx=5)

        tools2 = ttk.Frame(self)
        tools2.grid(row=13, column=0, columnspan=3, pady=5)
        ttk.Button(
            tools2, text="CREATE CINEMATIC VIDEO",
            command=self.render
        ).pack(side="left", padx=5, ipadx=30, ipady=7)

        self.status = tk.StringVar(
            value="Ready — verify a real full-body presenter, generate narration, then render."
        )
        ttk.Label(
            self, textvariable=self.status, wraplength=860, justify="left"
        ).grid(row=14, column=0, columnspan=3, padx=20, pady=10)

        ttk.Label(
            self,
            text="Graphic modes: LCD • room • title • lower-third • thumbnail • presenter intake",
            foreground="gray"
        ).grid(row=15, column=0, columnspan=3, pady=7)

    def _pick(self, key, types):
        p = filedialog.askopenfilename(filetypes=types)
        if p:
            self.vars[key].set(p)

    def verify_presenter(self):
        source = self.vars["presenter"].get().strip()
        if not source:
            messagebox.showerror("Missing presenter", "Select the full-body realistic presenter image first.")
            return
        destination = str(ROOT / "assets" / "presenter-verified.png")
        if Path(destination).exists():
            messagebox.showerror("Safety gate", "Verified presenter already exists. Choose a new source/output or remove it manually.")
            return
        cmd = [
            sys.executable, str(PRESENTER_VERIFY),
            "--source", source, "--destination", destination
        ]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if p.returncode == 0:
            self.vars["presenter"].set(destination)
            self.status.set("PASS: full-body presenter asset verified and normalized.")
            messagebox.showinfo("Presenter QA PASS", destination)
        else:
            self.status.set((p.stderr or p.stdout).strip()[-1400:])
            messagebox.showerror("Presenter verification failed", self.status.get())

    def generate_voice(self):
        text = self.script.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Missing narration", "Enter the narration script first.")
            return

        output = self.vars["voice"].get().strip()
        if not output:
            output = str(ROOT / "output" / "narration-v2.mp3")
            self.vars["voice"].set(output)
        if Path(output).exists():
            messagebox.showerror("Safety gate", "That audio file already exists. Choose a new filename.")
            return

        engine = self.vars["voice_engine"].get()
        if engine == "ElevenLabs":
            cmd = [
                sys.executable, str(VOICE_ELEVEN),
                "--text", text,
                "--output", output,
                "--voice-id", self.vars["eleven_voice_id"].get().strip(),
                "--model-id", self.vars["eleven_model"].get().strip(),
            ]
        else:
            cmd = [
                sys.executable, str(VOICE_EDGE),
                "--text", text,
                "--output", output,
            ]

        self.status.set(f"Generating {engine} narration locally/through configured provider…")
        self.update_idletasks()
        try:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if p.returncode == 0 and Path(output).exists():
                self.status.set(f"PASS: narration created → {output}")
                messagebox.showinfo("Voice QA PASS", output)
            else:
                detail = (p.stderr or p.stdout).strip()[-1600:]
                self.status.set(detail)
                messagebox.showerror("Voice generation failed", detail)
        except FileNotFoundError as exc:
            messagebox.showerror("Voice adapter missing", str(exc))

    def open_graphic_studio(self):
        if not GRAPHICS.exists():
            messagebox.showerror("Graphic Studio missing", f"Could not find {GRAPHICS}")
            return
        messagebox.showinfo(
            "Local Graphic Studio",
            "The upgraded studio now covers LCD/room/title/lower-third/thumbnail assets.\n\n"
            "Presenter images are handled by the Presenter QA gate: the software will "
            "verify and normalize a real full-body image, but it will not fabricate a fake human."
        )

    def render(self):
        presenter = self.vars["presenter"].get().strip()
        voice = self.vars["voice"].get().strip()
        lcd = self.vars["lcd"].get().strip()
        background = self.vars["background"].get().strip()
        output = self.vars["output"].get().strip()

        if not presenter or not voice or not output:
            messagebox.showerror("Missing input", "Presenter, voice and a new output path are required.")
            return
        if Path(output).exists():
            messagebox.showerror("Safety gate", "That output already exists. Choose a new filename.")
            return

        cmd = [
            sys.executable, str(PIPELINE),
            "--presenter", presenter,
            "--voice", voice,
            "--output", output,
            "--motion", self.vars["motion"].get(),
        ]
        if lcd:
            cmd += ["--lcd", lcd]
        if background:
            cmd += ["--background", background]

        self.status.set("Rendering locally with FFmpeg and running final media QA…")
        self.update_idletasks()
        try:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if p.returncode == 0:
                self.status.set(p.stdout.strip() or "PASS: render complete")
                messagebox.showinfo("QA PASS", "Cinematic presenter video created successfully.")
            else:
                self.status.set((p.stderr or p.stdout).strip()[-1600:])
                messagebox.showerror("Render failed", self.status.get())
        except FileNotFoundError:
            messagebox.showerror("Pipeline missing", f"Could not find {PIPELINE}")


if __name__ == "__main__":
    Studio().mainloop()
