#!/usr/bin/env bash
# 빈 Builder를 새로 띄우고 Studio 장면을 모두 녹화한다. Studio 두 개는 미리 띄워 둔다:
#   실제 연동: VITE_USE_REAL_BUILDER=true VITE_BUILDER_API_URL=http://localhost:8010 VITE_DEV_BYPASS_AUTH=true npx vite --port 5199
#   데모 모드: VITE_USE_REAL_BUILDER=false npx vite --port 5198
#
#   BUILDER_DIR=... STUDIO_DIR=... bash record-all.sh <out-dir> [scene ...]
set -euo pipefail
: "${BUILDER_DIR:?}" "${STUDIO_DIR:?}"
OUT=$1; shift
HERE=$(cd "$(dirname "$0")" && pwd)
pat="kpubdata-builder serve --port 80""10"
pkill -f "$pat" || true
sleep 1
WORK=$(mktemp -d "${TMPDIR:-/tmp}/kpd-builder-XXXX")
BUILDER_DIR=$BUILDER_DIR WORK=$WORK bash "$HERE/serve-builder.sh" > "$WORK/serve.log" 2>&1 &
BPID=$!
trap 'kill $BPID 2>/dev/null || true; pkill -f "$pat" || true' EXIT
until curl -sf localhost:8010/healthz > /dev/null; do sleep 0.5; done
NODE_PATH="$STUDIO_DIR/node_modules" node "$HERE/record.cjs" "$OUT" "$@"
