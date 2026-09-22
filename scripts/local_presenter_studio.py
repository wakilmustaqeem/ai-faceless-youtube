#!/usr/bin/env python3
"""Local Cinematic Presenter Studio — a small offline GUI for the FM presenter pipeline.

Requires Python 3 + Tkinter. Rendering still uses the existing local FFmpeg pipeline.
Nothing is uploaded and existing output files are never overwritten.
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "scripts" / "local_presenter_pipeline.py"

class Studio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI & IT Future Tech — Cinematic Presenter Studio")
        self.geometry("760x430")
        self.resizable(False, False)
        self.vars = {k: tk.StringVar() for k in ("presenter","voice","lcd","output")}
        self.vars["output"].set(str(ROOT / "output" / "cinematic-presenter-review.mp4"))
        self._build()

    def _row(self, label, key, types, r):
        ttk.Label(self, text=label).grid(row=r, column=0, sticky="w", padx=14, pady=10)
        ttk.Entry(self, textvariable=self.vars[key], width=68).grid(row=r, column=1, padx=8)
        ttk.Button(self, text="Browse", command=lambda: self._pick(key, types)).grid(row=r, column=2, padx=10)

    def _build(self):
        ttk.Label(self, text="Local Cinematic Presenter Studio", font=("TkDefaultFont", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(18, 8))
        ttk.Label(self, text="Offline/free-first • FFmpeg compositor • Main remains untouched").grid(
            row=1, column=0, columnspan=3, pady=(0, 12))
        self._row("Full-body presenter", "presenter", [("Images","*.png *.jpg *.jpeg"),("All files","*.*")], 2)
        self._row("Natural voice", "voice", [("Audio","*.mp3 *.wav *.m4a *.aac"),("All files","*.*")], 3)
        self._row("72-inch LCD artwork", "lcd", [("Images","*.png *.jpg *.jpeg"),("All files","*.*")], 4)
        self._row("New output file", "output", [("MP4","*.mp4"),("All files","*.*")], 5)
        ttk.Button(self, text="CREATE CINEMATIC VIDEO", command=self.render).grid(
            row=6, column=0, columnspan=3, pady=22, ipadx=24, ipady=8)
        self.status = tk.StringVar(value="Ready — choose presenter + voice; LCD is optional.")
        ttk.Label(self, textvariable=self.status, wraplength=700).grid(row=7, column=0, columnspan=3, padx=20)

    def _pick(self, key, types):
        p = filedialog.askopenfilename(filetypes=types)
        if p: self.vars[key].set(p)

    def render(self):
        presenter, voice, lcd, output = [self.vars[k].get().strip() for k in ("presenter","voice","lcd","output")]
        if not presenter or not voice or not output:
            messagebox.showerror("Missing input", "Presenter, voice and a new output path are required.")
            return
        if Path(output).exists():
            messagebox.showerror("Safety gate", "That output already exists. Choose a new filename.")
            return
        cmd = [sys.executable, str(PIPELINE), "--presenter", presenter, "--voice", voice, "--output", output]
        if lcd: cmd += ["--lcd", lcd]
        self.status.set("Rendering locally with FFmpeg…")
        self.update_idletasks()
        try:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if p.returncode == 0:
                self.status.set(p.stdout.strip() or "PASS: render complete")
                messagebox.showinfo("QA PASS", "Cinematic presenter video created successfully.")
            else:
                self.status.set((p.stderr or p.stdout).strip()[-1200:])
                messagebox.showerror("Render failed", self.status.get())
        except FileNotFoundError:
            messagebox.showerror("Pipeline missing", f"Could not find {PIPELINE}")

if __name__ == "__main__":
    Studio().mainloop()
