#!/usr/bin/env bash
# Remotion으로 렌더해 제출 파일을 만든다. 공고 조건에 따라 음성·음향·BGM이 없으므로 오디오 트랙을
# 만들지 않는다(--muted). 메타데이터를 지우고, 자막(.srt)과 썸네일(1280×720)을 같이 만든다.
#
#   cd hanium-dreamup/video/render && bash ../build-final.sh [out-dir]
set -euo pipefail
OUT=${1:-out/final}
NAME=kpubdata-dreamup-2026
mkdir -p "$OUT" public/brand
cp ../PretendardVariable.woff2 public/
cp ../symbol_light.svg public/brand/
npx remotion render src/index.ts Main out/render.mp4 --muted --concurrency=4 --log=error
ffmpeg -v error -y -i out/render.mp4 -map 0:v -c:v copy -an -map_metadata -1 -metadata:s:v:0 handler_name= \
  -movflags +faststart "$OUT/${NAME}_1080p.mp4"
python3 ../make_srt.py > "$OUT/$NAME.ko.srt"
npx remotion still src/index.ts Main "$OUT/${NAME}_thumbnail.png" --frame=60 --scale=0.6667 --log=error
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate -of compact "$OUT/${NAME}_1080p.mp4"
