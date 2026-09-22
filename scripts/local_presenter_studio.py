#!/usr/bin/env python3
"""AI & IT Future Tech — Cinematic Presenter Studio v2."""
from __future__ import annotations

import os
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
PRESENTER_GENERATOR = ROOT / "scripts" / "local_presenter_generator.py"


class Studio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI & IT Future Tech — Cinematic Presenter Studio v2")
        self.geometry("980x900")
        self.resizable(False, False)
        self.vars = {k: tk.StringVar() for k in (
            "presenter", "voice", "lcd", "background", "output",
            "voice_engine", "eleven_voice_id", "eleven_model", "motion",
            "model_path", "presenter_output"
        )}
        self.vars["output"].set(str(ROOT / "output" / "cinematic-presenter-review-v2.mp4"))
        self.vars["voice_engine"].set("Edge-TTS")
        self.vars["eleven_voice_id"].set("JBFqnCBsd6RMkjVDRZzb")
        self.vars["eleven_model"].set("eleven_multilingual_v2")
        self.vars["motion"].set("slow-push")
        self.vars["model_path"].set(os.getenv("PRESENTER_MODEL_PATH", ""))
        self.vars["presenter_output"].set(str(ROOT / "assets" / "presenter-generated-v2.png"))
        self._build()

    def _row(self, label, key, types, r):
        ttk.Label(self, text=label).grid(row=r, column=0, sticky="w", padx=14, pady=5)
        ttk.Entry(self, textvariable=self.vars[key], width=72).grid(row=r, column=1, padx=8)
        ttk.Button(self, text="Browse", command=lambda: self._pick(key, types)).grid(row=r, column=2, padx=10)

    def _build(self):
        ttk.Label(self, text="Local Cinematic Presenter Studio v2", font=("TkDefaultFont", 17, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(14, 4))
        ttk.Label(self, text="Presenter Generator + QA + ElevenLabs/Edge-TTS + Graphics + FFmpeg • Main untouched").grid(
            row=1, column=0, columnspan=3, pady=(0, 9))

        self._row("Full-body presenter asset", "presenter",
                  [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 2)

        ttk.Label(self, text="Presenter generation prompt").grid(row=3, column=0, sticky="nw", padx=14, pady=5)
        self.prompt = tk.Text(self, width=72, height=5, wrap="word")
        self.prompt.grid(row=3, column=1, padx=8, pady=5)
        self.prompt.insert("1.0",
            "photorealistic full-body adult technology presenter, standing naturally, "
            "professional modern outfit, realistic proportions, natural skin texture, "
            "friendly confident expression, cinematic studio lighting, feet visible, "
            "clean professional technology studio, no text, no logo")

        self._row("Local diffusion model path", "model_path",
                  [("All files", "*.*")], 4)
        self._row("Generated presenter output", "presenter_output",
                  [("PNG", "*.png"), ("All files", "*.*")], 5)

        gen = ttk.Frame(self)
        gen.grid(row=6, column=0, columnspan=3, pady=7)
        ttk.Button(gen, text="GENERATE FULL-BODY PRESENTER", command=self.generate_presenter).pack(side="left", padx=5)
        ttk.Button(gen, text="VERIFY PRESENTER", command=self.verify_presenter).pack(side="left", padx=5)

        ttk.Label(self, text="Narration script").grid(row=7, column=0, sticky="nw", padx=14, pady=5)
        self.script = tk.Text(self, width=72, height=6, wrap="word")
        self.script.grid(row=7, column=1, padx=8, pady=5)
        self.script.insert("1.0",
            "Welcome to AI and IT Future Tech. Today we are exploring how AI is changing the way we build, learn, and work.")

        ttk.Label(self, text="Voice engine").grid(row=8, column=0, sticky="w", padx=14, pady=5)
        ttk.Combobox(self, textvariable=self.vars["voice_engine"],
                     values=("Edge-TTS", "ElevenLabs"), state="readonly", width=69).grid(
            row=8, column=1, padx=8, sticky="w")
        ttk.Label(self, text="ElevenLabs voice ID").grid(row=9, column=0, sticky="w", padx=14, pady=5)
        ttk.Entry(self, textvariable=self.vars["eleven_voice_id"], width=72).grid(row=9, column=1, padx=8)
        ttk.Label(self, text="ElevenLabs model").grid(row=10, column=0, sticky="w", padx=14, pady=5)
        ttk.Entry(self, textvariable=self.vars["eleven_model"], width=72).grid(row=10, column=1, padx=8)

        self._row("Generated natural voice", "voice",
                  [("Audio", "*.mp3 *.wav *.m4a *.aac"), ("All files", "*.*")], 11)
        self._row("72-inch LCD artwork", "lcd",
                  [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 12)
        self._row("Cinematic background", "background",
                  [("Images", "*.png *.jpg *.jpeg"), ("All files", "*.*")], 13)
        self._row("New output file", "output",
                  [("MP4", "*.mp4"), ("All files", "*.*")], 14)

        ttk.Label(self, text="Motion").grid(row=15, column=0, sticky="w", padx=14, pady=5)
        ttk.Combobox(self, textvariable=self.vars["motion"],
                     values=("static", "slow-zoom", "slow-push", "pan-left", "pan-right"),
                     state="readonly", width=69).grid(row=15, column=1, padx=8, sticky="w")

        tools = ttk.Frame(self)
        tools.grid(row=16, column=0, columnspan=3, pady=10)
        ttk.Button(tools, text="GENERATE NATURAL VOICE", command=self.generate_voice).pack(side="left", padx=5)
        ttk.Button(tools, text="OPEN GRAPHIC STUDIO", command=self.open_graphic_studio).pack(side="left", padx=5)
        ttk.Button(tools, text="CREATE CINEMATIC VIDEO", command=self.render).pack(
            side="left", padx=5, ipadx=28, ipady=7)

        self.status = tk.StringVar(value="Ready — generate/verify presenter, generate voice, then render.")
        ttk.Label(self, textvariable=self.status, wraplength=900, justify="left").grid(
            row=17, column=0, columnspan=3, padx=20, pady=9)
        ttk.Label(self, text="No overwrite • no automatic publishing • Main untouched", foreground="gray").grid(
            row=18, column=0, columnspan=3, pady=6)

    def _pick(self, key, types):
        p = filedialog.askopenfilename(filetypes=types)
        if p:
            self.vars[key].set(p)

    def generate_presenter(self):
        model = self.vars["model_path"].get().strip()
        output = self.vars["presenter_output"].get().strip()
        prompt = self.prompt.get("1.0", "end").strip()
        if not model:
            messagebox.showerror("Local model required",
                                 "Select an already-installed local diffusion model. The tool will not download one.")
            return
        if not output or Path(output).exists():
            messagebox.showerror("Safety gate", "Choose a new presenter output filename that does not already exist.")
            return
        cmd = [sys.executable, str(PRESENTER_GENERATOR),
               "--model", model, "--output", output, "--prompt", prompt]
        self.status.set("Generating full-body presenter with the installed local model…")
        self.update_idletasks()
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if p.returncode == 0:
            self.vars["presenter"].set(output)
            self.status.set("PASS: local full-body presenter generated.")
            messagebox.showinfo("Presenter generated", output)
        else:
            detail = (p.stderr or p.stdout).strip()[-1600:]
            self.status.set(detail)
            messagebox.showerror("Presenter generation failed", detail)

    def verify_presenter(self):
        source = self.vars["presenter"].get().strip()
        if not source:
            messagebox.showerror("Missing presenter", "Select or generate the full-body presenter first.")
            return
        destination = str(ROOT / "assets" / "presenter-verified.png")
        if Path(destination).exists():
            messagebox.showerror("Safety gate", "Verified presenter already exists. No overwrite.")
            return
        p = subprocess.run([sys.executable, str(PRESENTER_VERIFY),
                            "--source", source, "--destination", destination],
                           cwd=ROOT, capture_output=True, text=True)
        if p.returncode == 0:
            self.vars["presenter"].set(destination)
            self.status.set("PASS: full-body presenter verified and normalized.")
            messagebox.showinfo("Presenter QA PASS", destination)
        else:
            detail = (p.stderr or p.stdout).strip()[-1400:]
            self.status.set(detail)
            messagebox.showerror("Presenter verification failed", detail)

    def generate_voice(self):
        text = self.script.get("1.0", "end").strip()
        output = self.vars["voice"].get().strip() or str(ROOT / "output" / "narration-v2.mp3")
        if not text:
            messagebox.showerror("Missing narration", "Enter the narration script first.")
            return
        if Path(output).exists():
            messagebox.showerror("Safety gate", "That audio already exists. Choose a new filename.")
            return
        engine = self.vars["voice_engine"].get()
        if engine == "ElevenLabs":
            cmd = [sys.executable, str(VOICE_ELEVEN), "--text", text, "--output", output,
                   "--voice-id", self.vars["eleven_voice_id"].get().strip(),
                   "--model-id", self.vars["eleven_model"].get().strip()]
        else:
            cmd = [sys.executable, str(VOICE_EDGE), "--text", text, "--output", output]
        self.vars["voice"].set(output)
        self.status.set(f"Generating {engine} narration…")
        self.update_idletasks()
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if p.returncode == 0 and Path(output).exists():
            self.status.set(f"PASS: narration created → {output}")
            messagebox.showinfo("Voice QA PASS", output)
        else:
            detail = (p.stderr or p.stdout).strip()[-1600:]
            self.status.set(detail)
            messagebox.showerror("Voice generation failed", detail)

    def open_graphic_studio(self):
        if not GRAPHICS.exists():
            messagebox.showerror("Graphic Studio missing", f"Could not find {GRAPHICS}")
            return
        messagebox.showinfo(
            "Graphic Studio",
            "Local graphic modes: LCD • room • title • lower-third • thumbnail. "
            "Presenter generation and verification are now integrated in this studio."
        )

    def render(self):
        presenter, voice = self.vars["presenter"].get().strip(), self.vars["voice"].get().strip()
        lcd, background, output = self.vars["lcd"].get().strip(), self.vars["background"].get().strip(), self.vars["output"].get().strip()
        if not presenter or not voice or not output:
            messagebox.showerror("Missing input", "Presenter, voice and a new output path are required.")
            return
        if Path(output).exists():
            messagebox.showerror("Safety gate", "That output already exists. Choose a new filename.")
            return
        cmd = [sys.executable, str(PIPELINE), "--presenter", presenter, "--voice", voice,
               "--output", output, "--motion", self.vars["motion"].get()]
        if lcd:
            cmd += ["--lcd", lcd]
        if background:
            cmd += ["--background", background]
        self.status.set("Rendering locally with FFmpeg and running final media QA…")
        self.update_idletasks()
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if p.returncode == 0:
            self.status.set(p.stdout.strip() or "PASS: render complete")
            messagebox.showinfo("QA PASS", "Cinematic presenter video created successfully.")
        else:
            detail = (p.stderr or p.stdout).strip()[-1600:]
            self.status.set(detail)
            messagebox.showerror("Render failed", detail)


if __name__ == "__main__":
    Studio().mainloop()
