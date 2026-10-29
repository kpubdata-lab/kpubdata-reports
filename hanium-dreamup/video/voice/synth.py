#!/usr/bin/env python3
"""Synthesizes the narration lines with Supertonic (local, CPU) and normalizes them.

    <supertonic-env>/bin/python synth.py <out-dir> [--voice F1] [--speed 1.0] [--only Q1,Q2]

Writes <out-dir>/<shot>.wav (48 kHz mono, silence trimmed, -16 LUFS, true peak -1.5 dBTP)
and <out-dir>/manifest.json with each line's duration. Same approach as the CUBRID Lab
introduction video (cubrid-lab/showcase, projects/cubrid-lab/intro-video/).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from supertonic import TTS

HERE = Path(__file__).resolve().parent
TARGET_I, TARGET_TP, TARGET_LRA = -16.0, -1.5, 7.0


def loudness(src: Path, pre: str) -> dict:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
         f"{pre},loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    return json.loads(out[out.rindex("{"):])


def postprocess(src: Path, dst: Path) -> None:
    trim = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse,"
            "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse")
    m = loudness(src, trim)
    norm = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:measured_I={m['input_i']}"
            f":measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                    f"{trim},{norm},aresample=48000:resampler=soxr", "-ar", "48000", "-ac", "1",
                    "-c:a", "pcm_s24le", str(dst)], check=True)


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--voice", default="F1")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--steps", type=int, default=16)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    only = {s for s in args.only.split(",") if s}
    lines = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))
    raw = args.out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    tts = TTS(model="supertonic-3")
    style = tts.get_voice_style(args.voice)
    shots = []
    for line in lines:
        if only and line["shot"] not in only:
            continue
        assert not re.search(r"[A-Za-z]", line["tts"]), f"{line['shot']}: spell Latin words in Hangul"
        wav, _ = tts.synthesize(line["tts"], style, total_steps=args.steps, speed=args.speed, lang="ko")
        r = raw / f"{line['shot']}.wav"
        tts.save_audio(wav, str(r))
        dst = args.out / f"{line['shot']}.wav"
        postprocess(r, dst)
        d = round(duration(dst), 3)
        shots.append({**line, "duration_s": d})
        print(line["shot"], d, flush=True)
    manifest = {"engine": "supertonic", "model": "supertonic-3", "voice": args.voice, "speed": args.speed,
                "steps": args.steps, "sample_rate": 48000, "loudness": {"I": TARGET_I, "TP": TARGET_TP},
                "shots": shots}
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
