#!/usr/bin/env python3
"""Check the storyboard of video-storyboard.md: timing and caption reading speed.

Reads the storyboard rows (``| <shot> | m:ss-m:ss | ...``) between the ``storyboard:main``
markers. Checks that the shots are contiguous, that the cut ends within 1:30 (the contest
limit), that each caption matches video/captions.json, and that no caption needs more than
MAX_CPS characters (spaces excluded) per second of the time it stays on screen.

    python3 hanium-dreamup/video_caption_budget.py

Exit status 1 on any problem. Standard library only. Adapted from the narration check of
the CUBRID Lab introduction video (cubrid-lab/showcase, projects/cubrid-lab/intro-video/).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC = HERE / "video-storyboard.md"
CAPTIONS = HERE / "video" / "captions.json"
MAX_CPS = 9.0
MAX_TOTAL = 90
ON_SCREEN_MARGIN = 10 / 30  # caption appears 6 frames after the cut and leaves 4 frames before the next

ROW = re.compile(r"^\|\s*([A-Z]\d)\s*\|\s*(\d+):(\d\d)[–-](\d+):(\d\d)\s*\|")


def main() -> int:
    errors: list[str] = []
    section = DOC.read_text(encoding="utf-8").split("<!-- storyboard:main -->", 1)[-1].split("<!-- /storyboard:main -->", 1)[0]
    captions = {c["shot"]: c["text"] for c in json.loads(CAPTIONS.read_text(encoding="utf-8"))}
    prev_end = 0
    seen = set()
    for line in section.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        shot, text = m[1], cells[5]
        start, end = int(m[2]) * 60 + int(m[3]), int(m[4]) * 60 + int(m[5])
        if start != prev_end:
            errors.append(f"{shot}: starts at {start}s, previous shot ends at {prev_end}s")
        prev_end = end
        if text in {"—", "-", ""}:
            if shot in captions:
                errors.append(f"{shot}: captions.json has a caption the storyboard does not")
            print(f"{shot}  {end - start:>2}s  —")
            continue
        seen.add(shot)
        if captions.get(shot) != text:
            errors.append(f"{shot}: storyboard caption differs from captions.json")
        chars = len(re.sub(r"\s", "", text))
        cps = chars / (end - start - ON_SCREEN_MARGIN)
        flag = "ok" if cps <= MAX_CPS else "FAST"
        if cps > MAX_CPS:
            errors.append(f"{shot}: {chars} chars in {end - start}s = {cps:.1f}/s > {MAX_CPS}/s")
        print(f"{shot}  {end - start:>2}s  {chars:>3} chars  {cps:4.1f}/s  {flag}")
    for shot in sorted(set(captions) - seen):
        errors.append(f"{shot}: in captions.json but not in the storyboard")
    print(f"total {prev_end // 60}:{prev_end % 60:02d} ({prev_end}s)")
    if prev_end > MAX_TOTAL:
        errors.append(f"cut length {prev_end}s is over {MAX_TOTAL}s")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
