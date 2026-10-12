"""제작설계서의 상세 절. build_design.py가 불러 쓴다."""
from docgen import c, fig, sheet, table, ul


def code(s):
    return f"<code>{s}</code>"


# 화면별 관련 API (화면 설계서의 '관련 API' 행)
SCREEN_API = {
    "로그인": "Keycloak 인증 서버 (Builder API 호출 없음)",
    "홈": "GET /datasets, GET /builds, GET /warehouse/tables, GET /analyses",
    "카탈로그": "GET /catalog, GET /datasets",
    "테이블 만들기": "POST /preview, POST /validate, POST /uploads, GET /datasets/{id}, POST /builds",
    "테이블": "GET /datasets, GET /warehouse/tables",
    "테이블 상세": "GET /warehouse/tables/{name}, GET /warehouse/tables/{name}/profile, POST /warehouse/rows, GET /datasets/{id}/quality/history",
    "SQL 작업 공간": "POST /warehouse/query, POST /warehouse/aggregate, POST /warehouse/exports, POST /analyses, POST /query",
    "저장된 분석": "GET /analyses, POST /analyses/{id}/run, DELETE /analyses/{id}",
    "작업대": "GET /datasets, GET /builds (저장한 BuildSpec은 브라우저 저장소)",
    "리포트": "GET /datasets, GET /datasets/{id}/runs 등 실행 근거 조회 (리포트 본문은 브라우저 저장소)",
    "갱신 이력": "GET /builds?limit=",
    "실행 상세": "GET /builds/{id}, GET /builds/{id}/stages, GET /builds/{id}/quality, GET /builds/{id}/events, GET /builds/{id}/spec, POST /builds/{id}/cancel",
    "산출물": "GET /builds/{id}/manifest, GET /artifacts/{id}, GET /artifacts/{id}/{path}",
    "게시": "GET /builds/{id}/publish/readiness, POST /builds/{id}/publish, POST /builds/{id}/publish/reconcile, DELETE /builds/{id}/publish/receipt",
    "품질": "GET /quality/summary, GET /quality/issues",
    "모니터링": "GET /monitoring/summary, GET /monitoring/builds",
    "연결": "GET /providers, POST /providers/{p}/test, POST /providers/{p}/probe, GET·PUT·DELETE /providers/{p}/credential",
    "설정": "GET /version, GET /providers",
    "Ask KPubData": "GET /catalog, GET /datasets/*, GET /builds/*, POST /query, POST /validate, 외부 LLM API",
    "관리": "GET /admin/config, GET /admin/runs, GET /admin/users, POST /admin/users/{id}/approve · reject",
}


# ---------------------------------------------------------------- 인터페이스 정의
def interface_sheets():
    head = ["영역", "메서드·경로", "용도"]
    w = ["24mm", "66mm", None]
    rows1 = [
        [c("상태", 4), code("GET /healthz") + " · " + code("/readyz"), "생존·준비 상태 확인 (인증 없음)"],
        [code("GET /version"), "API 계약 버전 조회"],
        [code("GET /metrics"), "Prometheus 형식 지표 (관리자 전용)"],
        [code("GET /monitoring/summary") + " · " + code("/monitoring/builds"), "API·대기열·작업자·저장소 상태, 시간대별 실행 통계"],
        [c("카탈로그·연결", 5), code("GET /catalog"), "제공 기관과 소스 데이터셋 목록"],
        [code("GET /providers"), "제공 기관과 설정 상태"],
        [code("POST /providers/{p}/test") + " · " + code("/probe"), "연결 확인, 데이터셋별 키 확인"],
        [code("GET /providers/{p}/status"), "호출자 자격 증명 기준 연결 상태"],
        [code("GET·PUT·DELETE /providers/{p}/credential"), "저장된 자격 증명 조회·등록·삭제"],
        [c("업로드", 2), code("POST /uploads"), "파일 소스용 파일 업로드"],
        [code("GET /uploads") + " · " + code("GET·DELETE /uploads/{id}"), "업로드 목록, 메타데이터 조회, 삭제"],
        [c("명세", 2), code("POST /validate"), "BuildSpec 검증"],
        [code("POST /preview"), "저장 없이 소스별 스키마·샘플 행 반환"],
        [c("실행", 10), code("POST /build"), "동기 실행. 요청 처리 중 파이프라인 수행"],
        [code("POST /builds"), "비동기 실행 제출. run_id 반환"],
        [code("GET /builds"), "실행 이력 목록"],
        [code("GET /builds/{id}"), "작업 상태 조회"],
        [code("POST /builds/{id}/cancel"), "협력적 취소"],
        [code("GET /builds/{id}/manifest"), "manifest.json 본문"],
        [code("GET /builds/{id}/spec"), "실행에 사용된 BuildSpec 스냅샷"],
        [code("GET /builds/{id}/events"), "실행 이벤트 타임라인"],
        [code("GET /builds/{id}/stages") + " · " + code("/stages/{stage}"), "Bronze·Silver·Gold 단계 상태와 상세"],
        [code("GET /builds/{id}/quality"), "실행의 품질 결과"],
    ]
    rows2 = [
        [c("산출물", 1), code("GET /artifacts/{id}") + " · " + code("/artifacts/{id}/{path}"), "실행 작업공간의 파일 목록, 파일 내려받기"],
        [c("테이블", 4), code("GET /datasets") + " · " + code("/datasets/{id}"), "생성 테이블 목록·요약"],
        [code("GET /datasets/{id}/runs") + " · " + code("/runs/{run}"), "테이블의 실행 이력"],
        [code("GET /datasets/{id}/quality/history"), "품질 이력"],
        [code("GET /quality/summary") + " · " + code("/quality/issues"), "품질 요약, 조치가 필요한 항목"],
        [c("웨어하우스", 6), code("GET /warehouse/tables") + " · " + code("/tables/{name}"), "커밋된 테이블, 조회 가능 스냅샷"],
        [code("GET /warehouse/tables/{name}/profile"), "스냅샷의 컬럼 프로파일"],
        [code("POST /warehouse/query"), "고정 스냅샷 대상 읽기 전용 SQL"],
        [code("POST /warehouse/rows"), "스냅샷 행 페이지 단위 조회"],
        [code("POST /warehouse/aggregate"), "검증된 집계"],
        [code("POST·GET /warehouse/exports") + ", " + code("/exports/{id}/download"), "질의 결과 내보내기 생성·목록·내려받기"],
        [c("질의·분석", 3), code("POST /query"), "실행의 Silver·Gold 표에 읽기 전용 SQL"],
        [code("GET·POST /analyses"), "저장된 분석 목록, 스냅샷에 고정해 저장"],
        [code("POST /analyses/{id}/run") + " · " + code("DELETE /analyses/{id}"), "저장 스냅샷 기준 재실행, 삭제"],
        [c("개정 이력", 2), code("PUT·GET /revisions/{kind}/{doc}"), "명세·주석의 새 개정 저장, 조회"],
        [code("GET …/history") + " · " + code("POST …/revert"), "개정 이력, 되돌리기"],
        [c("게시", 4), code("GET /builds/{id}/publish/readiness"), "게시 준비 상태와 차단 사유"],
        [code("POST /builds/{id}/publish"), "게시 실행"],
        [code("GET·DELETE /builds/{id}/publish/receipt"), "게시 영수증 조회·초기화"],
        [code("POST …/publish/reconcile") + " · " + code("GET …/publish/audit"), "대상과 대조, 감사 기록"],
        [c("관리", 3), code("GET /admin/config"), "현재 적용 중인 정책"],
        [code("GET /admin/runs"), "전체 사용자의 실행 (메타데이터)"],
        [code("GET /admin/users") + ", " + code("POST …/approve · reject"), "가입 신청 목록, 승인·거절"],
    ]
    common = ul([
        "계약 버전 1.123.0, 연산 77개. 계약 원본은 <code>contract/builder-api.yaml</code> (OpenAPI)",
        "인증: <code>X-API-Key</code> 또는 <code>Authorization: Bearer</code> (OIDC JWT). <code>/healthz</code>, <code>/readyz</code>만 무인증 응답",
        "제공 기관 키 전달: <code>X-Provider-Key</code> (미리보기·실행·연결 확인), 게시 자격 증명: <code>X-Publish-Credential</code>",
        "Studio는 계약 버전 1.96.0 이상, 주 버전 일치 시에만 호환으로 판단",
        "Studio는 전체 응답을 Zod 스키마로 검증, 형식 불일치 시 계약 불일치 오류 처리",
    ])
    return [
        sheet("인터페이스 정의서 - Builder HTTP API (1/2)", table(head, rows1, "small", w)),
        sheet("인터페이스 정의서 - Builder HTTP API (2/2)", table(head, rows2, "small", w)),
        sheet("인터페이스 정의서 - 공통 규칙", common),
    ]


# ---------------------------------------------------------------- 상태 전이
def state_sheets():
    return [sheet("기능 처리도 - 비동기 실행 상태 전이", fig("flow-state.svg", "비동기 실행 상태 전이") + table(["상태", "의미"], [
        [c(code("queued")), "대기열 등록 후 실행 대기"],
        [c(code("running")), "소스 수집 및 단계 수행 중"],
        [c(code("cancelling")), "취소 요청 접수, 다음 단계 경계에서 종료 대기"],
        [c(code("succeeded")), "전체 소스 성공 및 테이블 커밋 완료"],
        [c(code("failed")), "소스 실행·조립 또는 테이블 커밋 실패"],
        [c(code("cancelled")), "사용자 요청에 의한 취소"],
    ], "small", ["30mm", None]) + "<h3>취소 규칙</h3>" + table(["요청 시점 상태", "결과", "HTTP"], [
        [c(code("queued")), "즉시 cancelled. 파이프라인 미실행", c("200")],
        [c(code("running")), "cancelling 전환 후 다음 단계 경계에서 cancelled", c("200")],
        [c(code("cancelling") + " · " + code("cancelled")), "변화 없음 (반복 요청 시 동일 결과)", c("200")],
        [c(code("succeeded") + " · " + code("failed")), "취소 불가", c("409")],
    ], "small", ["44mm", None, "16mm"]) + ul([
        "취소는 협력적 방식으로 처리. 작업 스레드 강제 종료 없이 Bronze·Silver·Gold·Export 단계 경계에서만 확인",
        "마지막 경계 통과 후 정상 종료 확정 시 이후 취소 요청은 409로 거절",
        "취소 시점까지 생성된 산출물은 <code>partial=true</code>인 Manifest와 함께 보존",
        "실행 제한 기본값: 동시 실행 2건, 사용자별 진행 중 2건, 대기 10건, 실행 시간 6시간",
        "Studio는 종료 상태 도달 시까지 800ms 간격으로 <code>GET /builds/{id}</code>를 조회",
    ]))]


# ---------------------------------------------------------------- 알고리즘 상세
def algorithm_detail_sheets():
    silver = table(["순서", "규칙", "명세 항목", "동작"], [
        [c("1"), "읽기 형식", code("read_as"), "지정 컬럼을 문자열로 읽기 (앞자리 0 보존 등)"],
        [c("2"), "결측 토큰", code("null_tokens") + ", " + code("column_null_tokens"), "'-', 'N/A' 등의 값을 결측으로 처리. 컬럼별 토큰은 전역 토큰에 추가 적용"],
        [c("3"), "컬럼 병합", code("coalesce"), "명칭만 다른 복수 컬럼을 단일 컬럼으로 병합. 값 불일치 시 실패"],
        [c("4"), "이름 변경", code("rename"), "원본 필드명을 표준 명칭으로 변경"],
        [c("5"), "자리 채움", code("zfill"), "지정 자릿수까지 좌측 0 채움 (행정 코드 등)"],
        [c("6"), "형 변환", code("casts"), "bool·date·datetime·float·int·str과 천 단위 쉼표 숫자(int_comma, float_comma). 변환 과정에서 값 손실 시 오류"],
        [c("7"), "파생 컬럼", code("derived"), "date_parts(연·월·일 3개 컬럼 → 날짜), join_key(여러 컬럼 → 조인 키)"],
    ], "small", ["12mm", "24mm", "46mm", None])
    quality = table(["규칙", "검사 내용", "기준"], [
        [code("required_column"), "필수 컬럼 존재 여부", "스키마 계약의 required"],
        [code("dtype"), "컬럼 자료형 일치 여부", "스키마 계약의 dtypes"],
        [code("max_duplicate_rate"), "중복 행 비율", "0~1 사이 상한"],
        [code("max_null_ratio"), "컬럼별 결측 비율", "컬럼별 상한"],
        [code("min_rows"), "최소 행 수", "하한"],
        [code("range"), "숫자 컬럼의 값 범위", "min·max (경계 포함)"],
        [code("compare_columns"), "두 컬럼의 대소·동일 관계", "eq·ne·gt·gte·lt·lte"],
    ], "small", ["40mm", None, "50mm"])
    pii = table(["종류", "검출 방법"], [
        ["주민등록번호", "하이픈 포함 형식 또는 13자리 숫자에 대해 날짜·검증 숫자 확인"],
        ["전화번호", "국내 전화번호 형식 정규식"],
        ["이메일", "이메일 형식 정규식"],
        ["사업자등록번호", "사업자등록번호 형식 정규식"],
        ["컬럼명", "성명·주소·연락처 등 개인정보 관련 명칭 포함 여부"],
    ], "small", ["34mm", None])
    refuse = table(["사유 코드", "발생 조건", "처리"], [
        [code("table_exists"), "신규 테이블 생성 요청 시 동일 이름 테이블 기존재", "커밋 미수행, 실패로 기록"],
        [code("empty_result"), "결과 0행이며 <code>allow_empty</code> 미설정", "기존 스냅샷 유지"],
        [code("conflict"), "실행 시작 시점 revision과 현재 revision 불일치", "선행 커밋 유지, 해당 커밋 거부"],
        [code("commit_failed"), "파일 이동·카탈로그 기록 중 오류", "실패로 기록, Manifest에 사유 기재"],
    ], "small", ["30mm", None, "50mm"])
    sqlrules = ul([
        "입력은 공백 불가, 64KiB 이하",
        "sqlglot으로 DuckDB 문법 분석. 구문 오류는 거부",
        "단일 문장만 허용, SELECT·CTE·집합 연산에 한정 (DDL·DML 불가)",
        "재귀 CTE 불가, <code>dataset</code>명칭의 CTE 불가",
        "<code>VALUES</code>, <code>UNNEST</code>, <code>LATERAL</code>, 테이블 함수, 표본 추출(<code>TABLESAMPLE</code>) 불가",
        "환경 조회 함수(<code>current_setting</code>, <code>getenv</code>, <code>version</code> 등 44종) 불가",
        "비결정 함수(<code>random</code>, <code>uuid</code>, <code>now</code> 등 18종) 불가",
        "실제 테이블 참조는 따옴표·스키마 지정 없는 <code>dataset</code> 1개만 허용",
        "검사 통과 문장은 주석을 제거한 표준형으로 재생성하여 실행, 원문은 DuckDB에 미전달",
        "검사는 3중 방어의 1단계. 이후 잠금 설정된 DuckDB 연결과 별도 자식 프로세스에서 실행",
    ])
    scrub = ul([
        "필드명이 키·토큰·시크릿에 해당하는 경우 값 제거 (<code>servicekey</code>, <code>api_key</code>, <code>*token</code>, <code>*secret</code>)",
        "본문 속 <code>key: value</code>, <code>key=value</code> 형태 제거",
        "24자 이상이며 무작위성이 높은(섀넌 엔트로피 4.0비트/문자 이상) 문자열 제거",
        "제거한 값은 자리표시자로 치환, 응답 수신 후 브라우저 내에서만 복원",
        "Builder에서 확인된 실행 ID·근거 ID는 제거 대상에서 제외",
    ])
    return [
        sheet("알고리즘 명세서 - Silver 정규화", "<p>○ 명세에 선언한 규칙에 한해 아래 순서로 적용 (미선언 변환은 미수행)</p>" + silver + ul([
            "정규화는 DuckDB SQL로 수행, 결과는 <code>silver/{source}/table.parquet</code>에 저장",
            "Silver는 행·컬럼 전체 보존. 선택·필터는 Gold에서 수행",
            "필수 컬럼과 자료형 검증, 통계(<code>stats.json</code>), 미리보기(<code>preview.json</code>) 생성",
        ]) + "<h3>품질 검사 규칙</h3>" + quality + ul([
            "결과는 <code>pass</code>·<code>warn</code>·<code>fail</code>. 규칙별 심각도(warn·fail)를 명세에서 지정",
            "fail 1건 이상 시 해당 소스를 Gold 진입 전 중단, warn은 기록 후 진행",
            "미평가 규칙은 통과로 간주하지 않고 결과에서 제외",
            "이전 실행 대비 컬럼 추가·삭제, 자료형 변경, 행 수 급변은 스키마 변화로 기록 (중단 사유 아님)",
        ])),
        sheet("알고리즘 명세서 - 개인정보 검사와 분할", "<h3>개인정보 검사</h3>" + pii + ul([
            "문자열 컬럼의 고유 값을 대상으로 검사",
            "정책(<code>pii.mode</code>): <code>block</code>은 검출 시 소스 중단, <code>warn</code>은 기록 후 진행, <code>allow</code>는 통과 (게시와 병행 불가)",
            "마스킹은 선언 기반: kpubdata 선언 개인정보 컬럼과 명세의 <code>gold.pii_columns</code>에 적용",
            "문자열은 <code>[masked]</code>, 그 외 자료형은 결측으로 치환",
            "<code>publish_unmasked</code>로 예외 지정한 컬럼은 Manifest에 경고로 기록",
        ]) + "<h3>분할</h3>" + ul([
            "<code>ratio</code>: 시드와 행 순번의 해시로 정렬 후 비율에 따라 분할 (hash-sort-v2). 동일 입력에 대해 동일 결과 보장, 건수 정확 일치",
            "<code>key</code>: 지정 컬럼의 값별로 분할. 결측은 <code>__null__</code>, 컬럼 부재는 <code>__missing__</code>",
            "분할 명칭은 자유 지정 (train·valid·test는 관례)",
            "비율 분할에서 시간 컬럼의 무작위 분할은 명세 검증 단계에서 차단 (time_column_random_split)",
            "결과는 <code>gold/{name}/splits/{split}.parquet</code>에 저장",
        ])),
        sheet("알고리즘 명세서 - 웨어하우스 커밋", "<p>○ 상태가 ok인 실행의 Gold를 읽기 전용 스냅샷으로 커밋하고 테이블의 현재 스냅샷 교체</p>" + ul([
            "스냅샷은 임시 위치에 기록 후 검증을 거쳐 <code>tables/{id}/snapshots/{id}/</code>로 이동, 읽기 전용 설정",
            "테이블별 revision 관리, 커밋 시 1 증가",
            "이전 스냅샷은 최근 3개까지 보관, 그 외 정리. 저장된 분석이 참조 중인 스냅샷은 정리 대상에서 제외",
        ]) + "<h3>커밋 거부 사유</h3>" + refuse + ul([
            "커밋은 전체 소스 종료 후 단일 스레드에서 수행. 실행 시작 시점에 확보한 revision과 비교하는 방식",
            "커밋을 Manifest 기록에 앞서 수행하여 커밋 실패 내역이 Manifest·인덱스에 반영되도록 구성",
        ])),
        sheet("알고리즘 명세서 - 읽기 전용 SQL 검사와 비밀값 제거", "<h3>읽기 전용 SQL 검사 (Builder)</h3>" + sqlrules + "<h3>LLM 전송 전 비밀값 제거 (Studio)</h3>" + scrub),
    ]


# ---------------------------------------------------------------- 수집 상세
def collection_detail_sheets():
    return [sheet("데이터 수집처리 정의서 - 소스 종류와 제한", table(["소스 종류", "입력", "형식", "제한·규칙"], [
        [c("public_api"), "kpubdata 제공 기관과 데이터셋, 수집 파라미터", "kpubdata 표준 레코드", "페이지 단위 수집 후 즉시 저장. <code>param_grid</code> 조합별 체크포인트. 제공 기관별 분당 호출 상한 설정 가능"],
        [c("file"), "<code>POST /uploads</code>로 올린 파일의 <code>upload_id</code>", "csv, json, jsonl, parquet", "<code>upload_id</code> 형식 검사, 인코딩 지정 가능 (기본 utf-8)"],
        [c("url"), "HTTPS 주소", "json, jsonl, csv", "GET만 허용, 인증 헤더 불가, 주소에 사용자 정보 불가. 연결 5초·읽기 15초, 리다이렉트 5회, 20MiB 이하. DNS 고정으로 내부망 접근 차단"],
    ], "small", ["22mm", "44mm", "34mm", None]) + "<h3>수집 기록 (provenance)</h3>" + ul([
        "소스별 수집 시각, 파라미터, 레코드 수, 체크섬을 <code>metadata.json</code>과 Manifest에 기록",
        "재실행(<code>retry_of</code>)은 1일 이내의 <code>param_grid</code> 체크포인트를 승계하여 완료된 조합의 재수집 생략",
        "승계 불가로 전체 재수집한 소스는 Manifest의 <code>checkpoints_not_reused</code>에 기록",
    ]) + "<h3>정기 수집 일정 (GitHub Actions)</h3>" + table(["분야", "주기", "상태"], [
        ["기상 예보", "3시간마다", c("운영")],
        ["부동산 실거래 (매매·전월세)", "매월 1~10일", c("운영")],
        ["관광 정보", "매주 월요일", c("운영")],
        ["의약품 안전 사용(DUR)", "매주 토요일", c("운영")],
        ["대기질", "수동 실행", c("일정 중지")],
    ], "small", [None, "44mm", "24mm"]) + ul([
        "각 일정은 공통 게시 작업(<code>publish-dataset.yml</code>)을 호출하여 Hugging Face에 게시",
        "대기질은 이용 조건 문제로 일정 실행을 중지하고 수동 실행만 유지",
        "게시 실패 시 이슈 자동 등록 또는 갱신",
        "신규 데이터셋 탐색, 활용 신청 승인 확인은 매일 1회 실행",
    ]))]


# ---------------------------------------------------------------- 프로그램 목록
def program_sheets():
    b1 = table(["기능ID", "패키지·모듈", "역할"], [
        [c("A02_B01~02"), code("spec/"), "BuildSpec 모델, YAML 로더, 검증기, 실행 스냅샷, 지문, 갱신 주기, param_grid"],
        [c("A02·A03"), code("pipeline/"), "오케스트레이터(run_build), 실행 문맥, 취소 계약, 미리보기, 내보내기, 실패 분류, 카드 자료"],
        [c("A01_B01"), code("stages/bronze/"), "소스 수집, 임시 기록, 체크포인트, 저장"],
        [c("A01_B02"), code("ingestion/"), "URL 수집(내부망 차단), 파일 읽기(csv·json·jsonl·parquet)"],
        [c("A02_B05"), code("stages/silver/") + ", " + code("tabular/"), "DuckDB 실행 환경, 적재, 정규화, 검증, 통계, 미리보기, 스키마 변화 감지"],
        [c("A02_B06"), code("quality/"), "품질 평가기와 결과 모델"],
        [c("A06_B01"), code("stages/silver/pii.py") + ", " + code("stages/gold/pii.py"), "개인정보 검사, 선언 컬럼 마스킹"],
        [c("A02_B07"), code("stages/gold/"), "선택, 분할, 조인, 패키지 구성, 저장"],
        [c("A03_B01"), code("stages/gold/card.py") + ", " + code("catalog_info.py"), "데이터셋 카드(README.md, card.json) 생성"],
        [c("A03_B02"), code("exporters/"), "csv, jsonl, parquet, markdown, huggingface, kaggle와 등록 체계"],
        [c("A03_B05"), code("publishers/"), "local, huggingface, kaggle"],
        [c("A03_B03"), code("manifest/") + ", " + code("events/"), "Manifest 모델·기록·출처·체크섬, 실행 이벤트와 종료 기록"],
        [c("A03_B04"), code("warehouse/"), "테이블 카탈로그(SQLite), 스냅샷 배치, 커밋, 정리, 백업"],
        [c("A06_B03"), code("query/"), "읽기 전용 SQL 검사, 격리 실행, 집계, 행 조회, 프로파일, 내보내기"],
        [c("A04·A08"), code("service/"), "HTTP 서버, 경로, 인증, 비동기 작업, 게시, 모니터링, 관리, 재배포 판정"],
        [c("A06_B04"), code("credentials/") + ", " + code("uploads/"), "자격 증명 암호화 저장, 업로드 저장"],
        [c("A01_B04"), code("agent/") + ", " + code("verify/"), "신규 데이터셋 탐색, 활용 신청 승인 확인, 명세 실검증"],
        [c("-"), code("store/"), "실행 인덱스, 상태 목록, 스키마 버전, 상태 백업·잠금"],
        [c("-"), code("egress.py") + ", " + code("rate_limit.py"), "제공 기관별 호출 상한, 분당 요청 제한"],
        [c("-"), code("retention.py") + ", " + code("replay.py") + ", " + code("diff.py"), "실행 보존 기간 정리, 고정 자료 재생, Manifest 비교"],
        [c("-"), code("settings_catalog.py") + ", " + code("logging_redaction.py"), "환경변수 목록, 로그에서 키 제거"],
        [c("-"), code("cli.py"), "명령줄 진입점 (kpubdata-builder)"],
    ], "small", ["24mm", "66mm", None])
    cli = table(["명령", "용도"], [
        [code("validate"), "BuildSpec YAML 검증"],
        [code("preview"), "산출물 기록 없이 스키마·샘플 행 확인"],
        [code("build"), "Medallion 파이프라인으로 BuildSpec 실행"],
        [code("publish"), "산출물을 로컬 또는 원격 대상에 게시"],
        [code("serve"), "Builder HTTP 서비스 실행"],
        [code("settings"), "적용 중인 설정 출력(비밀값 마스킹) 및 점검"],
        [code("fixtures export"), "재생용 고정 자료를 지정 디렉터리로 복사"],
        [code("rebuild-index"), "파일 스캔을 통한 실행 인덱스 재구성"],
        [code("discover") + " · " + code("monitor") + " · " + code("pipeline"), "data.go.kr 메타데이터 탐색, 활용 신청 승인 확인, 신규 데이터셋 온보딩 자동화"],
        [code("verify"), "데이터셋 명세를 실제 API로 검증"],
        [code("prune-cancelled") + " · " + code("prune-runs"), "취소된 부분 실행, 보존 기간 경과 실행 정리"],
        [code("delete-user"), "사용자 및 관련 데이터 단계별 삭제"],
        [code("warehouse-gc") + " · " + code("warehouse-hold"), "불필요 스냅샷 정리, 스냅샷 보존 지정"],
        [code("warehouse-backup") + " · " + code("warehouse-restore"), "테이블 카탈로그와 스냅샷 파일 백업·복원"],
        [code("backup") + " · " + code("verify-backup") + " · " + code("restore"), "전체 상태 백업, 백업 검증, 복원"],
    ], "small", ["66mm", None])
    s1 = table(["기능ID", "디렉터리 (src/features)", "역할"], [
        [c("A04_B01"), code("home") + ", " + code("onboarding"), "홈 데이터(조치 필요, 연결 문제, 최근 스냅샷), 첫 실행 체크리스트, 활용 신청 안내"],
        [c("A04_B02"), code("discover"), "카탈로그 조회, 평탄화·필터, 비교 표"],
        [c("A04_B02"), code("add-data"), "테이블 만들기 마법사 3단계, 초안 저장, 기존 테이블 확인, 자격 증명 선행 조건, 업로드"],
        [c("A04_B02"), code("preview") + ", " + code("validation"), "<code>/preview</code>, <code>/validate</code> 클라이언트"],
        [c("A04_B02"), code("build-spec"), "Studio↔Builder 명세 변환, YAML, 실행별 명세 보관, 초안, 비교, 개정 이력, 편집 6단계"],
        [c("A04_B03"), code("datasets") + ", " + code("data-table"), "테이블 목록 모델, 실행 이력, 웨어하우스 보기, 프로파일, 품질 추세, 공통 표, 행 조회"],
        [c("A04_B04"), code("sql") + ", " + code("charts") + ", " + code("export"), "SQL 실행, 저장된 분석, 테이블 탐색기, 집계 차트, 내보내기"],
        [c("A04_B05"), code("reports") + ", " + code("workspace"), "리포트 저장소·근거·내보내기·편집기, 최근 작업, 저장한 BuildSpec"],
        [c("A04_B06"), code("runs") + ", " + code("artifacts"), "비동기 실행과 상태 조회, 이벤트 조회, 실행 상세, 산출물"],
        [c("A04_B06"), code("publish"), "게시 클라이언트, 데이터 카드 미리보기, 복구 패널"],
        [c("A04_B07"), code("provider") + ", " + code("version-check"), "연결 표, 키 확인, Builder 버전·계약 비교, 불일치 배너"],
        [c("A06_B02"), code("licence"), "이용 조건 요약, 실행별 라이선스"],
        [c("A06_B04"), code("auth"), "Keycloak 연동, 토큰 갱신, 로그인 보호, 사용자별 저장소 분리"],
        [c("A07_B01"), code("assistant"), "Ask KPubData: 서랍·본문, 세션, 키 설정, 프롬프트, 구조 검증, 근거 대조, 동작, 질의, 비밀값 제거"],
        [c("A08_B01"), code("monitoring") + ", " + code("admin"), "모니터링 모델과 패널, 관리자 판별과 관리 화면"],
        [c("A08_B02"), code("quality"), "품질 모델(PASS·WARN·FAIL·N/A), 항목 표, 배지"],
    ], "small", ["22mm", "52mm", None])
    pages = table(["파일 (src/pages)", "화면", "경로"], [
        [code("LoginPage") + " · " + code("SignupPage"), "로그인, 가입", code("/login") + ", " + code("/signup")],
        [code("HomePage"), "홈", code("/")],
        [code("DiscoverPage"), "카탈로그", code("/discover")],
        [code("AddDataPage"), "테이블 만들기", code("/add")],
        [code("DatasetCatalogPage") + " · " + code("DatasetDetailPage"), "테이블, 테이블 상세", code("/tables") + ", " + code("/tables/:id")],
        [code("SqlWorkspacePage") + " · " + code("AnalysesPage"), "SQL 작업 공간, 저장된 분석", code("/sql") + ", " + code("/analyses")],
        [code("WorkspacePage"), "작업대", code("/workspace")],
        [code("ReportsPage") + " · " + code("ReportEditorPage"), "리포트 목록, 편집기", code("/reports") + ", " + code("/reports/:id")],
        [code("BuildsPage"), "갱신 이력, 실행 상세", code("/refresh-jobs") + ", " + code("/refresh-jobs/:id")],
        [code("NewBuildPage"), "명세 편집·재실행", code("/refresh-jobs/:id/edit")],
        [code("BuildArtifactsPage") + " · " + code("BuildPublishPage"), "산출물, 게시", code("…/artifacts") + ", " + code("…/publish")],
        [code("QualityPage") + " · " + code("MonitoringPage"), "품질, 모니터링", code("/quality") + ", " + code("/monitoring")],
        [code("ProviderPage") + " · " + code("SettingsPage"), "연결, 설정", code("/connections") + ", " + code("/settings")],
        [code("AdminPage") + " · " + code("AssistantPage"), "관리, Ask KPubData", code("/admin") + ", " + code("/assistant")],
    ], "small", ["66mm", "46mm", None])
    stack = table(["구분", "내용"], [
        [c("Builder"), "Python 3.10~3.13, DuckDB 1.2 이상, pyarrow, SQLite, sqlglot, uv"],
        [c("Studio"), "React 19.3, TypeScript 6, Vite 8, React Router 7, Zustand 5, Tailwind CSS 4, Zod 4, react-hook-form, yaml"],
        [c("다국어"), "i18next, 한국어(기본)·영어"],
        [c("인증"), "Keycloak, keycloak-js (OIDC Authorization Code + PKCE)"],
        [c("실행 환경"), "Node 22.13 이상, Docker (Studio는 nginx 이미지로 제공)"],
    ], "small", ["24mm", None])
    return [
        sheet("프로그램 목록 - KPubData Builder", b1),
        sheet("프로그램 목록 - Builder CLI", cli + ul([
            "실행 파일명은 <code>kpubdata-builder</code>",
            "<code>validate</code>·<code>preview</code>·<code>build</code>는 HTTP 서비스와 동일한 파이프라인 호출",
        ])),
        sheet("프로그램 목록 - KPubData Studio", s1 + ul([
            "기능 폴더별 Builder용·데모용 클라이언트 구성, 동일 계약 테스트로 검증",
            "Builder API 호출은 <code>shared/lib/builderApi.ts</code>로 일원화",
        ])),
        sheet("프로그램 목록 - Studio 화면과 개발 스택", pages + "<h3>개발 스택</h3>" + stack),
    ]


# ---------------------------------------------------------------- 테이블 정의서
def table_sheets():
    hw = ["48mm", "40mm", None]
    spec = table(["필수/선택", "필드명", "타입", "설명"], [
        [c("필수"), code("dataset_id"), "string", "데이터셋 식별자"],
        [c("필수"), code("title"), "string", "사람이 읽는 제목"],
        [c("필수"), code("description"), "string", "목적과 데이터 설명"],
        [c("필수"), code("sources[]"), "array&lt;SourceRef&gt;", "입력 소스 (1개 이상)"],
        [c("선택"), code("exports[]"), "array&lt;ExportTarget&gt;", "내보내기 대상. 생략 시 테이블 커밋까지 수행"],
        [c("선택"), code("splits"), "SplitSpec", "분할 정의. 생략 시 분할 미수행"],
        [c("선택"), code("quality"), "QualityPolicy", "품질 기준. 생략 시 검사 미수행"],
        [c("선택"), code("pii"), "PiiPolicy", "개인정보 검사 정책. 생략 시 검사 미수행"],
        [c("선택"), code("composition"), "CompositionSpec", "두 소스를 조인하여 단일 Gold 생성"],
        [c("선택"), code("license"), "string", "SPDX 식별자 또는 자유 기재. 게시 시 필수"],
        [c("선택"), code("license_name") + " · " + code("license_link"), "string", "license가 other인 경우의 명칭·조건 링크"],
        [c("선택"), code("attribution"), "string", "출처 표기 문구. 카드의 출처 항목에 표시"],
        [c("선택"), code("publish"), "boolean", "실행 후 게시 여부 (기본 false)"],
        [c("선택"), code("refresh_cadence"), "string", "갱신 주기 (ISO-8601 기간: P1D, PT6H, P1W). 갱신 지연 판정에 사용"],
        [c("선택"), code("metadata"), "object", "산출물에 포함할 임의 메타데이터"],
    ], "small", ["18mm", "50mm", "36mm", None])
    source = table(["필드명", "타입 (기본값)", "설명"], [
        [code("kind"), "string (public_api)", "소스 종류: public_api | file | url"],
        [code("provider") + " · " + code("dataset"), "string", "kpubdata 제공 기관과 데이터셋. public_api에서 필수"],
        [code("params"), "object", "수집 파라미터"],
        [code("param_grid"), "object", "파라미터 축. 조합별 개별 수집"],
        [code("alias"), "string", "출력 키 명칭. 조인에서 참조"],
        [code("schema"), "SchemaContract", "Silver 정규화·검증 계약"],
        [code("gold"), "GoldSelection", "Gold 유지 대상 컬럼·행. 생략 시 Silver 전체"],
        [code("upload_id") + " · " + code("format") + " · " + code("encoding"), "string (encoding: utf-8)", "파일 소스: 업로드 식별자, 형식, 인코딩"],
        [code("endpoint") + " · " + code("method"), "string (method: GET)", "URL 소스: 주소, 메서드"],
        [code("allow_empty"), "boolean (false)", "0행 결과의 기존 테이블 대체 허용 여부"],
    ], "small", ["58mm", "38mm", None])
    schema = table(["필드명", "타입", "설명"], [
        [code("required"), "tuple&lt;string&gt;", "필수 컬럼"],
        [code("dtypes"), "dict", "컬럼별 기대 자료형"],
        [code("casts"), "dict", "컬럼별 형 변환"],
        [code("rename"), "dict", "원본 필드명 → 표준 명칭"],
        [code("derived"), "tuple&lt;DerivedColumn&gt;", "파생 컬럼 (name, kind, columns)"],
        [code("read_as"), "dict", "읽기 형식 지정 (str만 허용)"],
        [code("null_tokens") + " · " + code("column_null_tokens"), "tuple · dict", "전역·컬럼별 결측 토큰"],
        [code("coalesce"), "dict", "복수 컬럼을 단일 컬럼으로 병합"],
        [code("zfill"), "dict", "좌측 0 채움 자릿수"],
    ], "small", hw)
    gold = table(["모델", "필드명", "타입", "설명"], [
        [c("GoldSelection", 4), code("select"), "tuple&lt;string&gt;", "유지 대상 컬럼과 순서. 생략 시 전체"],
        [code("filters"), "tuple&lt;GoldFilter&gt;", "행 필터. select에 앞서 적용"],
        [code("pii_columns"), "tuple&lt;string&gt;", "개인정보 선언 컬럼"],
        [code("publish_unmasked"), "tuple&lt;string&gt;", "마스킹 제외 게시 대상 컬럼 (Manifest 경고 기록)"],
        [c("GoldFilter", 1), code("column") + " · " + code("op") + " · " + code("value"), "string · string · any", "연산: eq, ne, gt, ge, lt, le, in, not_null"],
        [c("ExportTarget", 1), code("kind") + " · " + code("output_path") + " · " + code("options"), "string · string · object", "내보내기 형식, 경로, 형식별 옵션"],
        [c("SplitSpec", 1), code("mode") + " · " + code("ratios") + " · " + code("key") + " · " + code("seed"), "string · dict · string · int", "ratio 또는 key 분할"],
        [c("PiiPolicy", 1), code("mode") + " · " + code("allow_columns"), "string · tuple", "block(기본) | warn | allow, 검사 예외 컬럼"],
    ], "small", ["26mm", "56mm", "42mm", None])
    quality = table(["모델", "필드명", "타입 (기본값)", "설명"], [
        [c("QualityPolicy", 5), code("max_duplicate_rate") + " (+ severity)", "float? (warn)", "중복 행 비율 상한"],
        [code("max_null_ratio") + " (+ severity)", "dict", "컬럼별 결측 비율 상한"],
        [code("min_rows") + " (+ severity)", "int? (warn)", "최소 행 수"],
        [code("range"), "tuple&lt;RangeRule&gt;", "값 범위 규칙"],
        [code("compare_columns"), "tuple&lt;CompareColumnsRule&gt;", "컬럼 비교 규칙"],
        [c("RangeRule", 1), code("column") + " · " + code("min") + " · " + code("max") + " · " + code("severity"), "string · float? · float? · string", "경계 포함 범위"],
        [c("CompareColumnsRule", 1), code("left") + " · " + code("operator") + " · " + code("right") + " · " + code("severity"), "string × 4", "연산: eq, ne, gt, gte, lt, lte"],
        [c("CompositionSpec", 1), code("name") + " · " + code("join"), "string · JoinSpec", "조인 결과 명칭, 조인 정의"],
        [c("JoinSpec", 5), code("left") + " · " + code("right"), "string", "조인할 두 소스의 alias"],
        [code("left_key") + " · " + code("right_key") + " 또는 " + code("keys"), "string · tuple", "단일 키 축약형 또는 복합 키 쌍 (택일)"],
        [code("type"), "string (inner)", "inner | left"],
        [code("cardinality"), "string?", "one_to_one | one_to_many | many_to_one | many_to_many"],
        [code("on_duplicate_key") + " · " + code("on_null_key"), "string (warn)", "키 중복·결측 시 warn | fail"],
    ], "small", ["32mm", "58mm", "40mm", None])
    manifest = table(["필드명", "타입", "설명"], [
        [code("build_id"), "string", "실행 식별자"],
        [code("started_at") + " / " + code("finished_at"), "datetime", "실행 시작·종료 시각"],
        [code("schema_version"), "string", "Manifest 형식 버전 (1.0.0)"],
        [code("status") + " · " + code("partial"), "string · bool", "ok | failed | cancelled. partial은 취소된 실행에서만 true"],
        [code("inputs") + " / " + code("outputs"), "tuple&lt;string&gt;", "소스 출력 키 / 생성된 산출물 경로"],
        [code("warnings") + " / " + code("errors"), "tuple&lt;string&gt;", "경고 / 실패 메시지"],
        [code("failures"), "tuple&lt;RunFailure&gt;", "실패 내역: source_key, stage, code, summary"],
        [code("row_counts"), "dict&lt;str,int&gt;", "소스·조인별 Silver 행 수"],
        [code("schema_summaries"), "dict", "소스별 스키마 요약"],
        [code("provenance"), "tuple&lt;SourceProvenance&gt;", "수집 시각, 파라미터, 레코드 수, 체크섬"],
        [code("quality_results"), "dict", "평가한 품질 검사 결과 (pass 포함)"],
        [code("schema_drift") + " · " + code("drift_evaluation"), "dict", "이전 실행 대비 변화, 축별 평가 여부"],
        [code("gold_selection"), "dict", "Silver 입력 행 수, Gold 출력 행 수, 적용 규칙"],
        [code("pii_masking"), "dict", "Gold별 마스킹한 컬럼과 예외 컬럼"],
        [code("composition"), "CompositionProvenance?", "조인 내역"],
        [code("warehouse_failures"), "dict", "커밋에 실패한 테이블과 사유"],
        [code("artifacts"), "dict", "Gold 디렉터리별 산출물 다이제스트와 작성기"],
        [code("build_environment"), "BuildEnvironment?", "Python·kpubdata·Builder 버전"],
        [code("inputs_fingerprint") + " (+ algorithm)", "string?", "입력 데이터 지문 (sha256:…)과 산출 방식"],
        [code("split_algorithm"), "string?", "비율 분할 알고리즘 (hash-sort-v2)"],
        [code("reproducibility") + " · " + code("checkpoints_not_reused"), "dict", "체크포인트 승계 소스, 전체 재수집 소스"],
        [code("created_by") + " · " + code("owner_id") + " · " + code("retry_of"), "string?", "요청자 표시명, 소유자(응답 제외), 재시도 대상 실행"],
    ], "small", ["56mm", "40mm", None])
    builds = table(["표", "컬럼", "설명"], [
        [c(code("builds")), "run_id (PK), status, started_at, finished_at, spec_digest, error, created_by, dataset_id, owner_id, error_code, error_stage", "실행 인덱스. status는 ok·failed·cancelled만 허용. finished_at·dataset_id 인덱스"],
        [c(code("build_events")), "seq, run_id, timestamp, event, status, source_key, stage, message, metrics", "실행 이벤트 타임라인"],
        [c(code("run_submissions")), "run_id (PK), owner_id, created_by, submitted_at", "비동기 제출 기록"],
        [c(code("run_endings")), "run_id (PK), status, stage, code, summary, recorded_at", "Manifest 생성 전 종료된 실행의 종료 기록"],
        [c(code("tables")), "id (PK), workspace_id, logical_name, current_snapshot_id, revision", "웨어하우스 테이블. (workspace_id, logical_name) 유일"],
        [c(code("table_snapshots")), "id (PK), table_id (FK), run_id, schema_version, coverage_hash, artifact_digest, row_count, state, created_at, committed_at, owner_id", "스냅샷. state: staging·validated·committed·quarantined·abandoned·retiring"],
        [c(code("analyses")), "analysis_id (PK), workspace_id, owner_id, name, sql, row_limit, table_name, snapshot_id, hold_id, result_meta, created_at", "저장된 분석. 조회 대상 스냅샷 정보 포함"],
    ], "small", ["30mm", "76mm", None])
    stores = table(["파일", "표", "용도"], [
        [code("_builds.sqlite"), "builds", "실행 인덱스 (Manifest로부터 재구성 가능)"],
        [code("_build_events.sqlite"), "build_events, run_submissions, run_endings", "실행 이벤트, 제출·종료 기록"],
        [code("_warehouse.sqlite"), "tables, table_snapshots, snapshot_leases, snapshot_holds", "웨어하우스 카탈로그와 스냅샷 보존"],
        [code("_publish_receipts.sqlite"), "publish_receipts, publish_receipt_audit", "게시 영수증과 감사 기록"],
        [code(".service/analyses.sqlite3"), "analyses", "저장된 분석"],
        [code(".service/revisions.sqlite3"), "revisions, revision_audit", "명세·주석 개정 이력"],
        [code(".service/uploads.sqlite3"), "uploads", "업로드 메타데이터 (대용량 본문은 파일 보관)"],
        [code(".service/provider-credentials.sqlite3"), "provider_credentials", "제공 기관 자격 증명 (암호화)"],
        [code(".service/provider_tests.sqlite3"), "provider_tests", "연결 확인 결과"],
        [code(".service/users.sqlite3"), "users", "가입 신청 원장"],
    ], "small", ["58mm", "58mm", None])
    codes = table(["검사 영역", "주요 오류 코드"], [
        ["필수 항목", "empty_field, missing_sources"],
        ["소스 식별", "empty_field, blank_alias"],
        ["내보내기", "unsupported_export_kind"],
        ["메타데이터", "empty_metadata_key"],
        ["분할", "missing_ratios, empty_ratio_name, ratio_sum_mismatch, empty_split_key, unsupported_split_mode, time_column_random_split"],
        ["스키마 계약", "unknown_dtype, unknown_cast_dtype, unknown_read_as_type 외 결측 토큰·병합·자리 채움·이름 변경·파생 규칙"],
        ["소스 종류", "unsupported_source_kind, invalid_upload_id, unsupported_source_format, unknown_encoding, unsupported_source_method, unsafe_url_scheme, url_userinfo_forbidden"],
        ["소스 키", "unsafe_alias, unsafe_source_key, duplicate_source_key, source_key_path_collision"],
        ["파라미터 축", "param_grid_not_supported, empty_param_grid_axis, param_grid_shadows_params, invalid_param_grid_value"],
        ["개인정보 정책", "pii_allow_with_publish"],
        ["라이선스", "missing_license_for_publish, license_other_needs_terms, license_terms_without_other"],
        ["품질", "empty_range_rule, inverted_range_rule, unknown_severity_column"],
        ["조인", "duplicate_source_alias, self_join, unknown_composition_source, duplicate_join_key_column, composition_name_collision"],
        ["Gold 선택", "gold_selection_with_composition"],
    ], "small", ["30mm", None])
    note = lambda src: ul([f"※ 출처: {src}"])
    return [
        sheet("테이블 정의서 - BuildSpec", "<p>○ BuildSpec 필드 구조 (dataset_id / title / description / sources[] 는 필수)</p>" + spec + ul([
            "※ DB 테이블이 아닌 실행 계약의 필드 구조를 테이블 정의서 형식으로 정리함 (출처: <code>spec/models.py</code>, <code>spec/loader.py</code>)",
            "이전 형식의 <code>normalization_mode</code>, <code>transforms</code>는 폐지되어 입력 시 로더에서 거부",
        ])),
        sheet("테이블 정의서 - SourceRef · SchemaContract", "<p>○ SourceRef — BuildSpec의 sources[] 항목</p>" + source + "<p>○ SchemaContract — 소스별 정규화·검증 계약 (모두 선택)</p>" + schema + note("<code>spec/models.py</code>")),
        sheet("테이블 정의서 - Gold · 내보내기 · 분할 · 개인정보", gold + note("<code>spec/models.py</code>, <code>spec/loader.py</code>")),
        sheet("테이블 정의서 - 품질 · 조인", quality + ul([
            "조인은 2개 소스 간 등가 조인 1건 지원",
            "심각도는 warn 또는 fail",
            "※ 출처: <code>spec/models.py</code>, <code>spec/loader.py</code>",
        ])),
        sheet("테이블 정의서 - BuildManifest", "<p>○ BuildManifest 필드 구조 — 파이프라인에 들어간 실행마다 1건 생성</p>" + manifest + note("<code>manifest/models.py</code>")),
        sheet("테이블 정의서 - SQLite 표", "<p>○ 주요 표와 컬럼</p>" + builds + note("<code>store/build_index.py</code>, <code>events/store.py</code>, <code>warehouse/catalog.py</code>, <code>service/analyses_api.py</code>")),
        sheet("테이블 정의서 - SQLite 저장소 목록", stores + ul([
            "실행 작업공간 <code>{output}/{run_id}/</code>에 manifest.json, buildspec.yaml, bronze/, silver/, gold/를 파일로 보관",
            "웨어하우스 스냅샷은 <code>{warehouse}/tables/{id}/snapshots/{id}/</code>에 Parquet으로 보관",
            "질의 결과 내보내기 파일은 <code>.service/exports/</code>에 보관",
        ]) + note("<code>store/build_index.py</code>, <code>events/store.py</code>, <code>warehouse/catalog.py</code>, <code>store/inventory.py</code>")),
        sheet("테이블 정의서 - 명세 검증 오류 코드", "<p>○ validate_spec이 반환하는 문제의 형식: code, path, message, hint</p>" + codes + ul([
            "검사는 실행 자원 생성 전 수행하며 문제 전체를 일괄 반환",
            "조인 키 존재 여부·자료형 호환은 실행 단계에서 확인 (검증 단계는 데이터 미조회)",
            "※ 출처: <code>spec/validator.py</code>",
        ])),
    ]


# ---------------------------------------------------------------- 테스트·배포
def test_deploy_sheets():
    tests = table(["대상", "종류", "규모·기준"], [
        [c("Builder", 4), "단위 테스트 (pytest)", "테스트 파일 271개"],
        ["통합·파이프라인 테스트", "통합 7개, 파이프라인 6개, 엔진 동등성 1개"],
        ["정적 검사", "ruff (lint·format), mypy (src 전체)"],
        ["실행 환경", "Python 3.10·3.11·3.12·3.13 각각 실행, 문서 빌드(mkdocs --strict)"],
        [c("Studio", 5), "단위 테스트 (Vitest)", "테스트 파일 308개. *.test.ts는 node, *.test.tsx는 jsdom 환경"],
        ["커버리지 기준", "구문 84%, 분기 75%, 함수 85%, 줄 86% 이상"],
        ["E2E (Playwright)", "스펙 26개. 데스크톱·모바일(Pixel 7)·CSP(운영 빌드) 프로젝트"],
        ["화면 기준 이미지", "5개 화면 × 3종(데스크톱, 390px, 다크) = 15장. 차이 200픽셀 이내"],
        ["접근성", "axe-core로 화면별 검사"],
        [c("연동", 2), "계약 호환", "Builder 계약과 Studio 스키마의 불일치 검사, kpubdata main과의 통합 테스트 (매일)"],
        ["실연동", "실제 Builder·다중 사용자·Keycloak 대상 E2E는 별도 설정으로 실행"],
    ], "small", ["20mm", "44mm", None])
    ci = table(["워크플로", "내용", "실행 시점"], [
        [code("ci.yml"), "lint, 형 검사, 테스트, 문서 빌드", "PR, main 푸시"],
        [code("security.yml"), "의존성 점검, 비밀값 검사, CodeQL", "PR, 푸시, 매주"],
        [code("docker.yml"), "서비스 이미지 빌드·검증·게시", "PR, 푸시, 버전 태그"],
        [code("cross-repo-contract.yml"), "kpubdata main과의 통합 테스트", "매일"],
        [code("image-rescan.yml"), "게시한 이미지 재검사", "매일"],
        [code("dataset-automation.yml"), "신규 데이터셋 탐색, 활용 신청 승인 확인", "매일"],
        [code("scheduled-*.yml"), "분야별 정기 수집·게시", "분야별 주기"],
        [code("release.yml"), "릴리스 준비와 태그", "수동"],
    ], "small", ["52mm", None, "36mm"])
    deploy = ul([
        "Builder: Docker 이미지로 HTTP 서비스 실행. 산출물·상태 정보는 <code>/data</code> 볼륨에 보관",
        "무인증 기동 불가 (API 키 또는 OIDC 필수). 개발 모드에 한해 인증 생략 가능",
        "설정은 환경변수로 주입: 인증·접근, 제공 기관 키, 실행·동시성, 업로드·URL 소스, 상태 저장·웨어하우스, 게시",
        "기동 시 설정 검사 수행, <code>settings</code> 명령으로 적용 값 확인",
        "제공 기관 자격 증명은 마스터 키로 암호화하여 저장",
        "Studio: 정적 빌드를 nginx 이미지로 제공. Builder 주소·OIDC 설정은 컨테이너 기동 시 주입 (<code>/config.js</code>)",
        "데모 모드: Builder 없이 고정 데이터로 동작, 전 화면 Demo 배지 표시",
    ])
    return [
        sheet("테스트 설계", tests + ul([
            "화면 기준 이미지는 고정 컨테이너에서 생성하여 글꼴·브라우저 차이 배제",
            "Studio의 기능별 클라이언트는 Builder용·데모용 모두 동일 계약 테스트 통과 필요",
        ])),
        sheet("CI·배포 구성", "<h3>GitHub Actions</h3>" + ci + "<h3>배포</h3>" + deploy),
    ]
