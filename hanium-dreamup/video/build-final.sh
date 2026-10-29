#!/usr/bin/env bash
# Remotion으로 렌더한 뒤 소리 크기를 맞추고(−14 LUFS, −1 dBTP) 메타데이터를 지워 제출 파일을 만든다.
# 자막(.srt)과 썸네일(1280×720)도 같이 만든다. video/render에서 실행한다.
#
#   cd hanium-dreamup/video/render && bash ../build-final.sh [out-dir]
set -euo pipefail
OUT=${1:-out/final}
NAME=kpubdata-dreamup-2026
mkdir -p "$OUT" public/brand
cp ../PretendardVariable.woff2 public/
cp ../symbol_light.svg public/brand/
npx remotion render src/index.ts Main out/render.mp4 --concurrency=4 --log=error

# 2-pass loudnorm: 첫 패스로 잰 값으로 둘째 패스를 선형 보정한다.
m=$(ffmpeg -hide_banner -nostats -i out/render.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
get() { echo "$m" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i out/render.mp4 -map 0:v -map 0:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -map_metadata -1 -metadata:s:v:0 handler_name= -metadata:s:a:0 handler_name= \
  -movflags +faststart "$OUT/${NAME}_1080p.mp4"

python3 ../make_srt.py > "$OUT/$NAME.ko.srt"
npx remotion still src/index.ts Main "$OUT/${NAME}_thumbnail.png" --frame=60 --scale=0.6667 --log=error
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$OUT/${NAME}_1080p.mp4"
ffmpeg -hide_banner -nostats -i "$OUT/${NAME}_1080p.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|True peak|Peak):" | head -3
