#!/usr/bin/env python3
"""Writes the Korean .srt from render/src/timeline.ts (shot lengths), voice/lines.json and the
synthesized line lengths (render/voice-manifest.json). Same timing as the burned-in subtitles."""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
ts = (HERE / "render/src/timeline.ts").read_text(encoding="utf-8")
offset = int(re.search(r"NARRATION_OFFSET = (\d+)", ts).group(1))
shots = re.findall(r"id: '(\w+)', dur: (\d+)", ts)
lines = {l["shot"]: l["display"] for l in json.loads((HERE / "voice/lines.json").read_text(encoding="utf-8"))}
dur = {s["shot"]: s["duration_s"] for s in json.loads((HERE / "render/voice-manifest.json").read_text(encoding="utf-8"))["shots"]}


def stamp(frame: int) -> str:
    ms = round(frame * 1000 / FPS)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


t, n = 0, 0
for sid, d in shots:
    if sid in lines:
        n += 1
        a = t + offset
        b = a + round(dur[sid] * FPS) + 6
        print(f"{n}\n{stamp(a)} --> {stamp(b)}\n{lines[sid]}\n")
    t += int(d)
