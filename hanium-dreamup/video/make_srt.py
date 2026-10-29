#!/usr/bin/env python3
"""Writes the Korean .srt from render/src/timeline.ts (shot lengths and caption margins) and
captions.json. Same timing as the burned-in subtitles."""

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
ts = (HERE / "render/src/timeline.ts").read_text(encoding="utf-8")
cin = int(re.search(r"CAPTION_IN = (\d+)", ts).group(1))
cout = int(re.search(r"CAPTION_OUT = (\d+)", ts).group(1))
shots = re.findall(r"id: '(\w+)', dur: (\d+)", ts)
text = {c["shot"]: c["text"] for c in json.loads((HERE / "captions.json").read_text(encoding="utf-8"))}


def stamp(frame: int) -> str:
    ms = round(frame * 1000 / FPS)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


t, n = 0, 0
for sid, d in shots:
    d = int(d)
    if sid in text:
        n += 1
        print(f"{n}\n{stamp(t + cin)} --> {stamp(t + d - cout)}\n{text[sid]}\n")
    t += d
