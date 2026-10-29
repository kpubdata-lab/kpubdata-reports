#!/usr/bin/env bash
# 녹화용 Builder를 띄운다. 단일 사용자 개발 모드(인증 생략), 게시 전 개인정보 검사 필수.
# 필요한 환경변수: KPUBDATA_DATAGO_API_KEY(공공데이터포털 키), HF_TOKEN(게시 준비 상태 점검용)
#
#   BUILDER_DIR=/path/to/kpubdata-builder WORK=/tmp/kpubdata-rec bash serve-builder.sh
set -euo pipefail
: "${BUILDER_DIR:?kpubdata-builder checkout}"
: "${WORK:?empty work directory for run workspaces and the warehouse}"
mkdir -p "$WORK/out" "$WORK/wh"
cd "$BUILDER_DIR"
export KPUBDATA_BUILDER_DEV_MODE=true
export KPUBDATA_BUILDER_ALLOWED_ORIGINS=http://localhost:5199
export KPUBDATA_BUILDER_REQUIRE_PII_SCAN_FOR_PUBLISH=true
exec .venv/bin/kpubdata-builder serve --port 8010 --output-dir "$WORK/out" --warehouse "$WORK/wh"
