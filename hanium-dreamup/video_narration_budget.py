#!/usr/bin/env python3
"""Check that every Korean narration line in video-storyboard.md fits its shot.

Reads the storyboard rows (``| <shot> | m:ss-m:ss | ...``) between the
``storyboard:main`` markers, spells product names the way the narrator reads
them (LEXICON), counts Korean syllables and compares them with the shot length
at the planning rate. It also checks that the shots are contiguous and that the
cut ends between 1:24 and 1:30.

    python3 hanium-dreamup/video_narration_budget.py

Exit status 1 if a line is over budget, a Latin word has no reading, or the
timeline is broken. Standard library only. Adapted from the CUBRID Lab
introduction video (cubrid-lab/showcase, projects/cubrid-lab/intro-video/).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOC = Path(__file__).with_name("video-storyboard.md")
RATE = 4.5  # planned Korean syllables per second of shot, leaving room for music
MIN_TOTAL, MAX_TOTAL = 84, 90

# How the narrator says each Latin token. Longest keys are replaced first.
LEXICON = {
    "Hugging Face": "허깅페이스",
    "KPubData": "케이퍼브데이터",
    "Builder": "빌더",
    "Studio": "스튜디오",
    "Bronze": "브론즈",
    "Silver": "실버",
    "Gold": "골드",
    "SQL": "에스큐엘",
    "AI": "에이아이",
}

ROW = re.compile(r"^\|\s*([A-Z]\d)\s*\|\s*(\d+):(\d\d)[–-](\d+):(\d\d)\s*\|")


def spoken(text: str) -> str:
    for key in sorted(LEXICON, key=len, reverse=True):
        text = re.sub(rf"(?<![A-Za-z0-9-]){re.escape(key)}(?![A-Za-z0-9-])", LEXICON[key], text)
    return text


def main() -> int:
    errors: list[str] = []
    rows = []
    doc = DOC.read_text(encoding="utf-8")
    section = doc.split("<!-- storyboard:main -->", 1)[-1].split("<!-- /storyboard:main -->", 1)[0]
    for line in section.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        start = int(m[2]) * 60 + int(m[3])
        end = int(m[4]) * 60 + int(m[5])
        rows.append((m[1], start, end, cells[5]))  # column 6: 내레이션

    if not rows:
        print(f"no storyboard rows found in {DOC}", file=sys.stderr)
        return 1

    total_syl = 0
    prev_end = 0
    for shot, start, end, narration in rows:
        if start != prev_end:
            errors.append(f"{shot}: starts at {start}s, previous shot ends at {prev_end}s")
        if start % 2 or end % 2:
            errors.append(f"{shot}: {start}-{end}s is off the 2-second bar grid")
        prev_end = end
        text = "" if narration in {"—", "-", ""} else spoken(narration)
        leftover = re.findall(r"[A-Za-z]+", text)
        if leftover:
            errors.append(f"{shot}: no reading for {leftover}; add it to LEXICON")
        syl = len(re.findall(r"[가-힣]", text))
        total_syl += syl
        budget = (end - start) * RATE
        flag = "OVER" if syl > budget else "ok"
        if syl > budget:
            errors.append(f"{shot}: {syl} syllables > budget {budget:.0f}")
        print(f"{shot}  {end - start:>3}s  {syl:>3} syl  budget {budget:>4.0f}  {syl / (end - start):.2f}/s  {flag}")

    total = prev_end
    print(f"total {total // 60}:{total % 60:02d} ({total}s), {total_syl} syllables, "
          f"{total_syl / total:.2f} syl/s overall")
    if not MIN_TOTAL <= total <= MAX_TOTAL:
        errors.append(f"cut length {total}s outside {MIN_TOTAL}-{MAX_TOTAL}s")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
