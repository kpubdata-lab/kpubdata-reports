#!/usr/bin/env python3
"""Synthesizes the 120 BPM background bed for the demo video (numpy only, deterministic).

    python3 generate.py <out.wav> [--seconds 88] [--seed 26]

1 bar = 2 s. Soft pad chords (C - G - Am - F), a gentle plucked arpeggio on eighths and a
quiet kick on beats 1 and 3, with a lift at the walkthrough (bar 14) and a resolve on the
end card. No samples, loops or recordings: every sound is made from oscillators and noise
here, so nothing can be Content ID claimed. Output: 48 kHz stereo 24-bit WAV via ffmpeg.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
BAR = 2.0
BEAT = BAR / 4

# Chords as MIDI notes, one per bar, in C major.
PROGRESSION = [
    [48, 55, 60, 64],  # C
    [43, 55, 59, 62],  # G
    [45, 57, 60, 64],  # Am
    [41, 53, 57, 60],  # F
]


def midi_hz(n: float) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def env_adsr(n: int, a: float, d: float, s: float, r: float) -> np.ndarray:
    t = np.arange(n) / SR
    total = n / SR
    e = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - s) * (t - a) / d, s))
    rel = np.clip((total - t) / r, 0, 1)
    return e * rel


def pad(freqs: list[float], dur: float, rng: np.random.Generator) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for f in freqs:
        for detune, pan in ((-0.12, 0.3), (0.12, 0.7)):
            ph = rng.uniform(0, 2 * np.pi)
            x = 0.6 * np.sin(2 * np.pi * (f + detune) * t + ph) + 0.25 * np.sin(2 * np.pi * 2 * (f + detune) * t + ph)
            out[:, 0] += x * (1 - pan)
            out[:, 1] += x * pan
    return out * env_adsr(n, 0.6, 0.4, 0.8, 0.6)[:, None] / len(freqs)


def pluck(f: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 18)
    return x * np.exp(-t * 6) * env_adsr(n, 0.004, 0.05, 1.0, 0.05)


def kick(dur: float = 0.35) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--seconds", type=float, default=88.0)
    ap.add_argument("--seed", type=int, default=26)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    total = args.seconds + 2.0
    n = int(total * SR)
    mix = np.zeros((n, 2))
    bars = int(np.ceil(args.seconds / BAR))

    def put(sig: np.ndarray, at: float, gain: float, pan: float = 0.5) -> None:
        i = int(at * SR)
        if i >= n:
            return
        sig = sig[: n - i]
        if sig.ndim == 1:
            sig = np.stack([sig * (1 - pan) * 2 ** 0.5 * 0.7, sig * pan * 2 ** 0.5 * 0.7], axis=1)
        mix[i : i + len(sig)] += sig * gain

    for b in range(bars):
        chord = PROGRESSION[b % 4]
        start = b * BAR
        last = b == bars - 1
        put(pad([midi_hz(m) for m in chord], BAR + (2.0 if last else 0.6), rng) * 0.22, start, 1.0)
        # Arpeggio from bar 2; fuller from the walkthrough (bar 14 = 0:28) to the recap (bar 40 = 1:20).
        if 1 <= b < bars - 1:
            notes = [chord[1] + 12, chord[2] + 12, chord[3] + 12, chord[2] + 12]
            density = 8 if 14 <= b < 40 else 4
            for k in range(density):
                put(pluck(midi_hz(notes[k % 4]), 0.6), start + k * BAR / density, 0.09 if density == 8 else 0.07,
                    0.35 + 0.3 * (k % 2))
        if 2 <= b < bars - 1:
            for beat in (0, 2):
                put(kick(), start + beat * BEAT, 0.16 if 14 <= b < 40 else 0.1)
        put(pluck(midi_hz(chord[0]), 1.2) * 0.8, start, 0.08)
    if bars > 1:
        put(pad([midi_hz(m) for m in (48, 55, 60, 64, 67)], 3.0, rng) * 0.2, (bars - 1) * BAR, 1.0)

    fade = np.ones(n)
    fi, fo = int(0.8 * SR), int(2.5 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    mix *= fade[:, None]
    mix /= max(1e-9, np.abs(mix).max()) / 0.7

    raw = args.out.with_suffix(".raw.f32")
    mix.astype("<f4").tofile(raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw),
                    "-af", "lowpass=f=6000,loudnorm=I=-20:TP=-2:LRA=7", "-ar", str(SR), "-c:a", "pcm_s24le", str(args.out)],
                   check=True)
    raw.unlink()


if __name__ == "__main__":
    main()
