"""제작설계서 HTML 생성. 출력: hanium-dreamup/design-document.html"""
import html
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "design-document.html"
BUILDER = "https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd"
STUDIO = "https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401"


from docgen import c, fig, sheet, table, ul
import design_detail as detail

parts = []

# ---------------------------------------------------------------- 표지
parts.append("""
<section class="sheet">
  <div class="cover-title" style="margin-top:60mm">
    <div class="name">SW개발/HW제작 설계서</div>
  </div>
  <div class="cover-meta">
    <div><strong>프로젝트 명 :</strong> 공공데이터 AI 데이터셋 자동 표준화 및 검증 플랫폼 개발</div>
    <div>2026. 09. 08 작성 · 2026. 10. 12 개정</div>
    <div>(26_HC277)</div>
  </div>
</section>
""")

# ---------------------------------------------------------------- 산출물
rows = [
    [c("환경 분석", 3), "시장/기술 환경 분석서", c("△"), c("△"), c("△"), c("수록")],
    ["설문조사 결과서", c("△"), c("△"), c("△"), c("-")],
    ["인터뷰 결과서", c("△"), c("△"), c("△"), c("-")],
    [c("요구사항 분석", 2), "요구사항 정의서", c("○"), c("○"), c("○"), c("수록")],
    ["유즈케이스 정의서", c("△"), c("△"), c("△"), c("-")],
    [c("아키텍처 설계", 4), "서비스 구성도(시스템 구성도)", c("○"), c("○"), c("○"), c("수록")],
    ["서비스 흐름도(데이터 흐름도)", c("△"), c("○"), c("△"), c("수록")],
    ["UI/UX 정의서", c("△"), c("△"), c("△"), c("-")],
    ["하드웨어/센서 구성도", c("-"), c("-"), c("○"), c("해당 없음")],
    [c("기능 설계", 7), "메뉴 구성도", c("○"), c("○"), c("○"), c("수록")],
    ["화면 설계서", c("○"), c("○"), c("△"), c("수록")],
    ["엔티티 관계도", c("○"), c("○"), c("△"), c("수록")],
    ["기능 처리도(기능 흐름도)", c("○"), c("○"), c("○"), c("수록")],
    ["알고리즘 명세서/설명서", c("△"), c("○"), c("○"), c("수록")],
    ["데이터 수집처리 정의서", c("-"), c("○"), c("-"), c("수록")],
    ["하드웨어 설계도", c("-"), c("-"), c("○"), c("해당 없음")],
    [c("개발 / 구현", 3), "프로그램 목록", c("○"), c("○"), c("○"), c("수록")],
    ["테이블 정의서", c("○"), c("○"), c("△"), c("수록")],
    ["핵심 소스코드", c("○"), c("○"), c("○"), c("수록")],
]
parts.append(sheet("수행 단계별 주요 산출물", table(
    ["단계", "산출물", "일반<br>(모바일 APP·Web 등)", "응용 소프트웨어<br>(빅데이터·인공지능 등)", "응용 하드웨어<br>(IoT·로봇 등)", "본 설계서"],
    rows, "small", ["22mm", None, "26mm", "30mm", "26mm", "20mm"]) + ul([
        "※ ○ 필수, △ 선택",
        "본 프로젝트는 응용 소프트웨어(빅데이터·인공지능) 유형으로, 필수 산출물 전체와 시장/기술 환경 분석서 수록",
        "전용 하드웨어 미사용으로 하드웨어 관련 산출물은 작성 대상에서 제외",
    ])))

# ---------------------------------------------------------------- 시장/기술 동향
market = ul([
    "AI 학습 데이터 시장은 2024년 약 26억 달러에서 2030년 86억 달러로 연평균 21.9% 성장 전망 (Grand View Research, 2025)",
    "생성형 AI·LLM 확산에 따라 출처와 품질이 검증된 학습·분석용 데이터 수요 증가",
    "국내 공공데이터는 OECD 공공데이터 평가(OURdata Index) 4회 연속 1위, 개방 건수 지속 증가",
    "개방 범위는 원천 API 제공까지이며, 분석·학습용 표 형태로의 가공은 이용자 부담",
    "→ 공공데이터를 수집·정제·검증하여 재사용 가능한 테이블·데이터셋으로 제공하는 도구 필요",
])
maturity = table(["단계", "정의", "개요"], [
    [c("Level 0"), "수동 처리", "개별 스크립트로 API 호출, 수기 정제. 표준·재현성 미확보"],
    [c("Level 1"), "부분 자동화", "수집·정제를 스크립트화. 형식 변환 일부만 자동화"],
    [c("Level 2"), "파이프라인화", "수집→정제→검증을 ETL 파이프라인으로 연결 (dbt·Airflow 등)"],
    [c("<strong>Level 3</strong>"), "<strong>선언적·재현 빌드</strong>", "<strong>명세(BuildSpec) 기반 실행, 출처·Manifest 기록, 스냅샷 관리, 다중 포맷 내보내기 ★ 본 프로젝트</strong>"],
    [c("Level 4"), "지능형 자동화", "스키마 자동 매핑, 품질 자동 개선, LLM 기반 데이터 큐레이션 (지향점)"],
], "small", ["18mm", "32mm", None])
compare = table(["기능", "본 프로젝트", "공공데이터 포털", "HF Datasets", "Kaggle", "dbt·ETL", "DVC"], [
    ["공공 API 직접 수집", c("○"), c("○"), c("×"), c("×"), c("△"), c("×")],
    ["자동 정규화·표준화", c("○"), c("×"), c("×"), c("×"), c("○"), c("×")],
    ["선언적 빌드(명세)", c("○"), c("×"), c("×"), c("×"), c("○"), c("△")],
    ["다중 포맷 내보내기", c("○"), c("△"), c("○"), c("△"), c("×"), c("×")],
    ["데이터셋 카드 자동 생성", c("○"), c("×"), c("△"), c("△"), c("×"), c("×")],
    ["재현성(Manifest·버전)", c("○"), c("×"), c("△"), c("×"), c("△"), c("○")],
    ["허브 배포(HF·Kaggle)", c("○"), c("×"), c("○"), c("○"), c("×"), c("×")],
    ["비개발자용 웹 UI", c("○"), c("△"), c("△"), c("○"), c("×"), c("×")],
    ["국내 공공데이터 특화", c("○"), c("○"), c("×"), c("×"), c("×"), c("×")],
], "small", [None, "20mm", "24mm", "20mm", "16mm", "16mm", "14mm"])
differ = table(["구분", "기존 접근", "본 프로젝트"], [
    [c("공공데이터 포털"), "원천 API 제공 중심. 분석·학습 적합성은 이용자가 직접 확인", "정제·검증·분할·문서화를 거친 테이블과 데이터셋으로 산출"],
    [c("범용 ETL 도구<br>(Airflow 등)"), "파이프라인 실행은 가능하나 도메인 지식·검증 규칙은 사용자가 직접 구현", "kpubdata가 제공하는 공공 API 접근 위에 스키마 계약·품질 규칙을 명세로 선언"],
    [c("데이터 허브<br>(Hugging Face 등)"), "배포·공유 중심. 생성 과정 미기록", "생성 규칙·실행 기록·입력 지문을 Manifest로 기록하고 카드와 함께 게시"],
    [c("일반 LLM 데이터 도구"), "LLM이 스키마·내용을 추정하여 생성", "LLM 답변을 Builder 근거와 대조하고 사용자 승인 후에만 실행"],
], "small", ["32mm", None, None])
parts.append(sheet("시장/기술 동향 분석", "<h3>1. 시장 동향</h3>" + market + "<h3>2. 기술 성숙도 단계</h3>" + maturity))
parts.append(sheet("시장/기술 동향 분석", "<h3>3. 경쟁 제품 비교</h3>" + compare + ul(["○ 제공, △ 일부 제공, × 미제공"]) + "<h3>4. 차별화 비교</h3>" + differ))

# ---------------------------------------------------------------- 요구사항
def req(rid, name, feats):
    out = []
    for i, (fid, fname, detail, exc, state) in enumerate(feats):
        row = []
        if i == 0:
            row += [c(f"<strong>{rid}</strong>", len(feats)), c(name, len(feats))]
        row += [c(fid), fname, detail, exc, c(state)]
        out.append(row)
    return out

R = []
R += req("A01", "데이터 수집", [
    ("A01_B01", "공공 API 수집", "kpubdata로 공공 API를 호출해 원천 레코드를 페이지 단위로 수집·저장", "수집 실패 시 해당 소스만 실패 처리, 나머지 소스는 계속 진행", "구현"),
    ("A01_B02", "파일·URL 수집", "업로드 파일(CSV·JSON·JSONL·Parquet)과 HTTPS URL(JSON·JSONL·CSV)을 소스로 사용", "비허용 형식·주소는 명세 검증 단계에서 거부", "구현"),
    ("A01_B03", "소스 카탈로그", "kpubdata에 등록된 제공 기관·데이터셋 목록을 조회", "조회 실패 시 오류 상태와 다시 시도 제공", "구현"),
    ("A01_B04", "정기 수집", "GitHub Actions 일정에 따라 분야별 데이터를 주기적으로 수집·게시", "실패 시 이슈를 자동 등록", "구현"),
])
R += req("A02", "데이터 가공·품질", [
    ("A02_B01", "BuildSpec 작성", "소스·스키마 계약·품질·분할·내보내기를 하나의 명세로 선언", "필수 항목 누락 시 실행 전 오류 목록 반환", "구현"),
    ("A02_B02", "BuildSpec 검증", "필수 항목, 소스 종류, 스키마 계약, 분할, 라이선스 등 15개 영역 검사", "위반 사항 전체를 code·path·message 형식으로 일괄 반환", "구현"),
    ("A02_B03", "결과 미리보기", "저장 없이 소스별 스키마와 샘플 행을 확인", "미리보기 실패 시 원인을 화면에 표시", "구현"),
    ("A02_B04", "Bronze 원천 보존", "수집한 원천 레코드와 수집 시각·파라미터·건수·체크섬을 보존", "저장 실패 시 해당 소스를 실패 처리", "구현"),
    ("A02_B05", "Silver 정규화", "DuckDB로 결측 토큰·컬럼 병합·이름 변경·자리 채움·형 변환·파생 컬럼을 순서대로 적용", "형 변환 과정에서 값 손실 발생 시 오류 처리", "구현"),
    ("A02_B06", "품질 검사", "필수 컬럼, 자료형, 중복률, 결측률, 최소 행 수, 값 범위, 컬럼 간 비교 검사", "fail은 Gold 진입 전 중단, warn은 기록 후 진행", "구현"),
    ("A02_B07", "Gold 선택·분할", "행 필터와 컬럼 선택, 비율·키 기준 분할, 두 소스 조인", "분할 비율 합계 불일치 시 검증 오류", "구현"),
])
R += req("A03", "산출물 생성·배포", [
    ("A03_B01", "데이터셋 카드", "스키마·샘플·출처·처리 내역·개인정보 항목을 담은 README.md와 card.json 생성", "필수 항목 누락 시 게시 차단", "구현"),
    ("A03_B02", "다중 포맷 내보내기", "CSV·JSONL·Parquet·Markdown·Hugging Face·Kaggle 형식으로 출력", "미등록 형식은 검증 단계에서 거부", "구현"),
    ("A03_B03", "Manifest 기록", "상태·입력·산출물·행 수·출처·품질 결과·실패 내역을 manifest.json으로 기록", "Manifest 생성 전 종료된 실행은 종료 기록으로 별도 보관", "구현"),
    ("A03_B04", "테이블 스냅샷", "성공한 실행의 Gold를 웨어하우스 스냅샷으로 커밋하고 최근 3개 유지", "동시 갱신 충돌 시 커밋 거부 및 사유 기록", "구현"),
    ("A03_B05", "외부 게시", "산출물을 로컬·Hugging Face·Kaggle로 게시. 준비 상태 점검 후 실행", "라이선스·개인정보 검사 미통과 시 게시 차단", "구현"),
])
R += req("A04", "웹 작업공간<br>(Studio)", [
    ("A04_B01", "홈", "조치가 필요한 테이블, 최근 스냅샷·분석, 연결 문제 표시", "조회 실패 시 영역별 오류 표시", "구현"),
    ("A04_B02", "카탈로그·테이블 만들기", "소스 검색 후 3단계 마법사로 테이블 생성", "검증 실패 시 실행 차단", "구현"),
    ("A04_B03", "테이블·테이블 상세", "스냅샷·스키마·프로파일·미리보기·품질 확인", "웨어하우스 미구성 시 실행 기준 보기로 전환", "구현"),
    ("A04_B04", "SQL 작업 공간", "스냅샷에 읽기 전용 SQL 실행, 분석 저장, 집계 차트, 결과 내보내기", "비허용 SQL은 Builder에서 거부", "구현"),
    ("A04_B05", "리포트", "실행 근거를 바탕으로 리포트 작성, Markdown·HTML 내려받기", "브라우저 저장 범위를 화면에 명시", "구현"),
    ("A04_B06", "갱신 이력·게시", "실행 목록·상세·산출물 확인, 재실행, Hugging Face 게시", "실행 실패 시 실패 단계와 코드 표시", "구현"),
    ("A04_B07", "연결·설정", "제공 기관 자격 증명 관리, Builder 연결 상태·버전 확인", "최소 계약 버전 미만 시 경고 배너 표시", "구현"),
])
R += req("A05", "운영 자동화", [
    ("A05_B01", "CI", "Builder: ruff·mypy·pytest(Python 3.10~3.13). Studio: ESLint·Vitest·Playwright", "검사 실패 시 병합 차단", "구현"),
    ("A05_B02", "계약 호환 점검", "Builder API 계약과 Studio 스키마의 불일치를 CI에서 검사", "불일치 시 실패", "구현"),
])
R += req("A06", "데이터 보안·거버넌스", [
    ("A06_B01", "개인정보 검사·마스킹", "주민등록번호·전화번호·이메일·사업자번호 패턴과 컬럼명 규칙으로 검사, 선언한 컬럼 마스킹", "block 모드에서 검출 시 해당 소스 중단", "구현"),
    ("A06_B02", "라이선스·재배포 판정", "소스별 재배포 조건(허용·비상업·금지·미확인) 중 가장 엄격한 값 적용", "게시할 때 라이선스 미기재면 검증 오류", "구현"),
    ("A06_B03", "읽기 전용 SQL 검사", "단일 SELECT만 허용, 테이블 함수·비결정 함수·외부 접근 차단", "위반 시 실행하지 않고 거부", "구현"),
    ("A06_B04", "인증·자격 증명", "OIDC(Keycloak) 로그인, 제공 기관 키 암호화 저장", "토큰 갱신 실패 시 로그인 화면으로 이동", "구현"),
])
R += req("A07", "AI 보조", [
    ("A07_B01", "Ask KPubData", "화면 문맥과 Builder 근거를 바탕으로 답변·SQL·다음 동작 제안", "근거 미확인 참조는 답변에서 제거", "구현"),
    ("A07_B02", "LLM 스키마 자동 매핑", "컬럼명을 표준 용어로 자동 매핑", "-", "제외"),
])
R += req("A08", "운영 관제·품질 시각화", [
    ("A08_B01", "모니터링", "API·대기열·작업자·스냅샷 저장소 상태와 24시간 실행 통계", "권한 미보유 시 안내 문구만 표시", "구현"),
    ("A08_B02", "품질 센터", "WARN·FAIL 결과와 스키마 변화를 테이블 전체에서 조회", "점수 산정 없이 검사 결과만 표시", "구현"),
])
R += req("A09", "버전 관리", [
    ("A09_B01", "스냅샷·명세 이력", "테이블 스냅샷 revision, 명세 개정 이력과 되돌리기", "충돌 시 최신 revision 기준으로 거부", "구현"),
])
head = ["요구사항ID", "요구사항명", "기능ID", "기능명", "세부사항", "예외사항", "상태"]
w = ["16mm", "22mm", "17mm", "27mm", None, "38mm", "11mm"]
parts.append(sheet("요구사항 정의서", table(head, R[:11], "small", w)))
parts.append(sheet("요구사항 정의서", table(head, R[11:23], "small", w)))
parts.append(sheet("요구사항 정의서", table(head, R[23:], "small", w) + ul([
    "A07_B02는 구현 범위에서 제외, 컬럼 대응은 명세의 rename·coalesce 선언으로 대체",
    "개인정보 검사는 규칙 기반, 버전 관리는 웨어하우스 스냅샷·명세 개정 이력 방식으로 구현",
])))

# ---------------------------------------------------------------- 서비스 구성도
parts.append(sheet("서비스 구성도 - 서비스 시나리오", fig("architecture.svg", "서비스 구성도", "tall")))
parts.append(sheet("서비스 구성도 - 서비스 시나리오", "<h3>1. 구성 요소</h3>" + table(["구성 요소", "역할"], [
    [c("KPubData Studio"), "웹 작업공간. 화면과 사용자 흐름 담당. 실행 기능 없이 Builder API만 호출"],
    [c("KPubData Builder"), "실행·웨어하우스 계층. 명세 검증, Bronze·Silver·Gold 실행, 스냅샷·Manifest 기록, 읽기 전용 SQL 제공"],
    [c("kpubdata"), "공공 API 접근 라이브러리. 제공 기관별 호출과 표준 레코드 변환 담당"],
    [c("저장소"), "실행 작업공간(로컬 파일), 웨어하우스 스냅샷(Parquet), SQLite 인덱스"],
    [c("외부 대상"), "Hugging Face·Kaggle 등 게시 대상, OIDC 인증 제공자(Keycloak)"],
], "", ["38mm", None]) + "<h3>2. 테이블 만들기 (Studio 기반)</h3>" + ul([
    "① 사용자가 Studio 카탈로그에서 소스를 선택하고 규칙(BuildSpec) 구성",
    "② Studio가 Builder API에 미리보기·검증을 요청하여 스키마와 샘플 확인",
    "③ 만들기 실행 시 Builder가 Bronze→Silver→Gold 순으로 가공 후 스냅샷·Manifest 생성",
    "④ 사용자는 테이블 상세, SQL 작업 공간, 리포트에서 결과 활용",
]) + "<h3>3. 정기 수집·게시 (일정 기반)</h3>" + ul([
    "① GitHub Actions 일정에 따라 분야별 수집 작업 주기 실행 (기상 3시간, 관광·의약품 주 1회, 부동산 월초)",
    "② kpubdata로 공공 API 데이터 수집, 게시 스크립트로 정제·패키징",
    "③ 검증 통과 데이터셋을 Hugging Face에 게시",
    "④ 실패 시 이슈 자동 등록으로 담당자 확인",
    "정기 게시는 기존 게시 스크립트 경로로 운영 중이며 BuildSpec 기반 경로로 순차 이전 예정",
])))

# ---------------------------------------------------------------- 서비스 흐름도
parts.append(sheet("서비스 흐름도", fig("flow-service.svg", "서비스 흐름도") + ul([
    "① 규칙 작성: 카탈로그에서 소스 선택 후 파라미터·규칙 입력",
    "② 미리보기·검증: Studio가 <code>POST /preview</code>, <code>POST /validate</code>를 동시에 요청",
    "③ 원천 조회: Builder가 kpubdata를 통해 공공 API 샘플 수신 후 표준 레코드로 변환",
    "④ 실행 제출: <code>POST /builds</code>로 비동기 제출하고 <code>run_id</code> 수신",
    "⑤ 진행 확인: <code>GET /builds/{run_id}</code>를 800ms 간격으로 조회 (탭 비활성 시 중단)",
    "⑥ 결과 확인: 실행 상세에서 단계별 상태·품질·이벤트 확인, 테이블 스냅샷 활용",
])))

parts += detail.interface_sheets()

# ---------------------------------------------------------------- 메뉴 구성도
parts.append(sheet("메뉴 구성도", fig("menu.svg", "메뉴 구성도", "m70") + table(["그룹", "메뉴", "경로", "설명"], [
    [c("-"), "홈", "<code>/</code>", "조치가 필요한 테이블과 최근 변경"],
    [c("데이터", 2), "카탈로그", "<code>/discover</code>", "공공 API 소스 데이터셋 탐색"],
    ["테이블", "<code>/tables</code>", "소스 기반으로 생성한 테이블 목록·상세"],
    [c("분석", 4), "SQL 작업 공간", "<code>/sql</code>", "테이블 스냅샷에 SQL 실행"],
    ["저장된 분석", "<code>/analyses</code>", "스냅샷에 고정해 저장한 분석"],
    ["작업대", "<code>/workspace</code>", "최근 작업과 저장한 BuildSpec"],
    ["리포트", "<code>/reports</code>", "근거 기반 리포트 작성"],
    [c("운영", 4), "갱신 이력", "<code>/refresh-jobs</code>", "테이블 생성·갱신 실행 기록"],
    ["품질", "<code>/quality</code>", "품질 검사 결과와 스키마 변화"],
    ["모니터링", "<code>/monitoring</code>", "Builder 상태와 실행 통계"],
    ["관리", "<code>/admin</code>", "운영 정책·전체 실행·가입 승인 (관리자 전용)"],
    [c("하단", 2), "연결", "<code>/connections</code>", "제공 기관 자격 증명"],
    ["설정", "<code>/settings</code>", "Builder 연결, 계정, AI 키"],
], "small", ["16mm", "30mm", "34mm", None]) + ul([
    "테이블 만들기(<code>/add</code>)는 별도 메뉴 없이 카탈로그·테이블 화면의 버튼으로 진입",
    "상단 바: 경로 표시, Demo·Beta 배지, 통합 검색(⌘K), Ask KPubData 버튼, 계정 메뉴",
    "이전 경로(<code>/datasets</code>, <code>/builds</code>, <code>/provider</code>, <code>/validate</code>, <code>/preview</code>, <code>/artifacts</code>)는 신규 경로로 자동 이동",
])))

# ---------------------------------------------------------------- 화면 설계서
SCREENS = [
    ("로그인", ["login.png"], "Keycloak 로그인 진입 화면",
     ["좌측 소개 영역: 제품 문구와 핵심 단계 배지 7종 (Source·BuildSpec·Preview·Validate·Build·Quality·AI)", "우측 로그인 카드: Google 로그인, 이메일 로그인 버튼"],
     ["로그인 버튼 클릭 시 Keycloak 인증 화면으로 이동 (OIDC Authorization Code + PKCE)", "데모 모드에서만 이메일·비밀번호 입력 폼 표시", "인증 완료 시 최초 요청 화면으로 이동"]),
    ("홈", ["home.png"], "조치가 필요한 테이블과 최근 변경 사항을 우선 표시하는 시작 화면",
     ["조치가 필요한 테이블 (최대 6개)", "최근 스냅샷 및 해당 실행 (최대 5개)", "최근 저장한 분석, 연결 문제", "상단 '새 SQL 쿼리' 버튼"],
     ["테이블·실행 이력이 없는 경우 첫 실행 체크리스트(이용 신청 → 키 등록 → 키 확인 → 첫 테이블) 표시", "웨어하우스 미구성 배포에서는 최근 스냅샷 대신 최근 실행 표시", "각 항목 클릭 시 해당 테이블·분석으로 바로 이동"]),
    ("카탈로그", ["catalog.png"], "Builder 제공 소스 데이터셋을 비교 표로 탐색하는 화면",
     ["검색창, 제공 기관 선택, '서비스 키 필요'·'활용 신청 필요' 체크박스", "비교 표: 소스, 제공 기관, 표현, 지원 동작, 접근 조건, 생성 테이블, 호출 한도, 시작", "상단 '테이블 만들기' 버튼"],
     ["필터 조건이 주소(<code>?q=&amp;provider=</code>)에 반영되어 공유 가능", "행의 시작 버튼 클릭 시 해당 소스가 입력된 상태로 테이블 만들기 진입", "로딩·오류(다시 시도)·결과 없음 상태를 구분하여 표시"]),
    ("테이블 만들기", ["add.png", "add-source.png"], "소스 선택부터 생성까지 3단계로 구성된 마법사",
     ["단계 표시: 구성 → 미리보기·검증 → 만들기", "1단계: 소스 종류 카드 3종(공공 API, 파일 업로드, URL / REST API)과 가져오기 설정", "2단계: 소스별 스키마·샘플과 검증 결과", "3단계: 최종 명세, 테이블 이름, 동일 이름 테이블 존재 안내", "하단: 이전, 초안 저장, 다음"],
     ["소스 종류 미선택 또는 명세 오류 시 다음 단계 진행 차단", "자격 증명 미등록 시 연결 화면으로 안내 후 복귀", "미리보기 결과가 최신이 아닌 경우 만들기 차단", "제출 수락 시 초안 정리 후 실행 상세로 이동"]),
    ("테이블", ["tables.png"], "생성한 테이블의 현재 스냅샷·상태를 확인하는 목록 화면",
     ["검색창, 제공 기관 선택, '조치 필요만' 필터", "표: 테이블, 스냅샷, 행 수, 상태, 완전성, 갱신, 마지막 갱신"],
     ["행 클릭 시 테이블 상세로 이동", "웨어하우스 미구성 시 스냅샷 열 숨김 및 안내 문구 표시", "테이블이 없는 경우 테이블 만들기 안내 표시"]),
    ("테이블 상세", ["table-detail.png"], "테이블 단위 스냅샷·스키마·품질을 탭으로 확인하는 화면",
     ["탭: 개요, 스키마, 프로파일, 미리보기, 품질, 스냅샷", "상단 동작: 이 테이블에 대해 질문, 갱신, 쿼리", "다중 소스 테이블은 소스 전환 기능 제공"],
     ["과거 스냅샷 조회 시 '현재로 돌아가기' 버튼 표시", "스냅샷 탭에서 실행 상세·명세 편집·게시로 이동", "커밋된 스냅샷이 없는 경우 실행 기준 보기(개요·스키마·미리보기·품질·실행)로 표시"]),
    ("SQL 작업 공간", ["sql.png"], "테이블 스냅샷 대상 읽기 전용 SQL 실행 화면",
     ["테이블 탐색기 (테이블 → 소스 → 컬럼)", "스냅샷 선택(기본값 현재), SQL 입력창, 실행 버튼", "결과 표(<code>table@snapshot · rev N</code>), 분석 저장, 집계 차트, 결과 내보내기"],
     ["⌘/Ctrl+Enter로 실행", "쿼리당 테이블 1개 조회", "기본 입력문: <code>SELECT * FROM dataset LIMIT 100</code>", "SQL 안전성 검사는 Builder가 수행"]),
    ("저장된 분석", ["analyses.png"], "스냅샷 고정 저장 분석의 재실행 화면",
     ["분석 카드: 이름, <code>table@snapshot</code>, 저장 정보", "버튼: 다시 실행, SQL 작업 공간에서 열기, 삭제"],
     ["저장된 분석이 없는 경우 SQL 작업 공간 안내 표시", "삭제 시 확인 절차 진행"]),
    ("작업대", ["workspace.png"], "최근 작업·저장 BuildSpec 통합 관리 화면",
     ["최근 작업 목록 (테이블·실행·리포트·저장한 명세)", "저장한 BuildSpec: 이름 변경, 복제, 삭제"],
     ["저장한 BuildSpec의 브라우저 한정 보관을 배지로 명시", "저장한 명세 선택 시 테이블 만들기로 이동"]),
    ("리포트", ["reports.png"], "실행 근거 기반 리포트 생성·편집 화면",
     ["새 리포트 만들기: 테이블·실행 선택", "리포트 목록: 열기, 이름 변경, 복제, 삭제", "편집기: 근거 영역(1~6), AI 분석(7), 사용자 메모(8), 자동 저장"],
     ["리포트의 브라우저 한정 저장을 배지로 명시", "근거 새로 고침, Markdown·HTML 내려받기, 인쇄 제공", "선택한 실행이 기준으로 고정되며 이후 실행이 추가되어도 자동 변경 없음"]),
    ("갱신 이력", ["refresh-history.png"], "테이블 생성·갱신 실행 이력 통합 조회 화면",
     ["검색창, 상태 필터(전체·성공·실패·실행 중·대기·취소), 테이블 필터", "표: 실행 ID, 테이블, 상태, 시작, 소요 시간, 스냅샷"],
     ["행 클릭 시 실행 상세로 이동", "'더 보기'로 이전 실행 추가 조회", "필터 조건은 주소에 반영"]),
    ("실행 상세", ["run-detail.png"], "실행 단위 단계별 결과·품질·이벤트 확인 화면",
     ["상단: 제목, 상태, 취소 버튼(진행 중일 때), 편집·산출물·게시 링크", "소스별 진행: Bronze → Silver → Gold → 출력", "품질 결과, 실패 근거, 실행 이벤트 타임라인, 명세 스냅샷"],
     ["진행 중에는 800ms 간격으로 상태 갱신, 이벤트는 3초 간격", "취소는 단계 경계에서 반영, 확인 절차 후 진행", "실행 없음·조회 실패·권한 없음 상태를 구분하여 안내"]),
    ("산출물", ["artifacts.png"], "실행 산출 파일과 Manifest 확인 화면",
     ["Manifest 요약, 내려받을 수 있는 파일 목록, manifest.json 원문"],
     ["영역별 개별 조회로 일부 영역 실패 시에도 나머지 영역 정상 표시", "파일 내려받기는 게시와 별개 기능으로 제공"]),
    ("게시", ["publish.png"], "실행 결과의 Hugging Face 게시 화면",
     ["게시 준비 상태 (차단 사유·경고)", "데이터 카드 미리보기", "대상 저장소(<code>owner/dataset</code>), 비공개 여부", "검토·확인 후 '지금 게시'"],
     ["차단 사유 존재 시 게시 버튼 비활성", "비상업 조건 데이터는 별도 확인 절차", "결과 불명확 시 자동 재시도 없이 복구 패널(대조·영수증 초기화) 제공"]),
    ("품질", ["quality.png"], "전체 테이블의 품질 경고·스키마 변화 통합 조회 화면",
     ["필터: 상태, 테이블, 분류", "표: 테이블, 소스, 규칙, 컬럼, 상태, 실제값 / 기준값, 영향 행 수, 스냅샷"],
     ["점수 대신 검사 결과(PASS·WARN·FAIL·N/A)만 표시", "각 행은 테이블 상세의 품질 탭으로 연결", "'도우미로 분석' 버튼 제공"]),
    ("모니터링", ["monitoring.png"], "Builder 상태·최근 24시간 실행 현황 확인 화면",
     ["Builder 상태: API, 대기열, 작업자, 스냅샷 저장소", "최근 24시간 실행 통계, 최근 갱신 목록", "자동 새로 고침 체크박스, 수동 새로 고침 버튼"],
     ["30초 간격 조회, 탭 비활성 시 중단", "권한 미보유 시 안내 문구만 표시", "일부 값 조회 실패 시 저하 상태 배너 표시"]),
    ("연결", ["connections.png"], "공공데이터 제공 기관 자격 증명 관리 화면",
     ["표: 제공 기관, 인증 방식, 설정 여부, 마지막 확인, 동작", "선택한 기관의 자격 증명 패널, 키 확인, 활용 신청 안내"],
     ["단일 사용자 배포: 키 저장·삭제", "다중 사용자 배포: 키를 현재 세션에 한해 사용 (메모리 보관)", "키 원문은 화면 미표시"]),
    ("설정", ["settings.png"], "Builder 연결·계정·AI 키 상태 확인 화면",
     ["연결: Builder 주소와 계약 버전 확인", "개인정보 안내, 계정, 제공 기관 자격 증명 요약", "Ask KPubData 키(BYOK) 상태"],
     ["Builder 계약 버전이 최소 요건(1.96.0) 미만인 경우 전 화면 경고 배너 표시", "AI 키는 기본 메모리 보관"]),
    ("Ask KPubData", [], "현재 화면의 테이블·실행·품질 문맥 기반 질의응답과 후속 동작 제안을 제공하는 AI 도우미",
     ["문맥 표시(테이블·실행·품질·단계), 추천 질문, 관련 데이터셋", "답변, 근거 목록, 생성된 SQL(실행·복사), 제안 동작(승인·거절)", "키 입력 폼: API 키, 모델, 주소"],
     ["우측 서랍 형태로 표시, 전체 화면(<code>/assistant</code>) 병행 제공", "SQL은 사용자가 실행 버튼을 선택한 경우에만 Builder로 전달", "문맥 변경 이후의 제안 동작은 실행 불가로 표시"]),
    ("관리", [], "운영 정책·전체 실행·가입 신청 확인용 관리자 화면",
     ["현재 적용 중인 정책", "전체 사용자의 실행 목록 (메타데이터만)", "가입 신청 목록: 승인, 거절"],
     ["관리자 계정에 한해 메뉴 표시", "카드별 로딩·권한 없음·미지원·실패 상태 개별 표시"]),
]
n = len(SCREENS)
for i, (name, imgs, purpose, elements, states) in enumerate(SCREENS, 1):
    shots = "".join(fig(f"screens/{f}", f"{name} 화면", "shot two" if len(imgs) > 1 else "shot") for f in imgs)
    info = ('<table class="info small">'
            f"<tr><th>화면 개요</th><td>{purpose}</td></tr>"
            f"<tr><th>주요 UI 구성요소</th><td>{ul(elements)}</td></tr>"
            f"<tr><th>상태·상호작용</th><td>{ul(states)}</td></tr>"
            f"<tr><th>관련 API</th><td><code>{detail.SCREEN_API[name]}</code></td></tr></table>")
    parts.append(sheet(f"화면 설계서 — {name} ({i}/{n})", shots + info))

# ---------------------------------------------------------------- 엔티티 관계도
parts.append(sheet("엔티티 관계도 - 핵심 도메인 모델", fig("entities.svg", "도메인 모델 클래스 다이어그램", "mid") + ul([
    "BuildSpec은 실행 입력을 선언하는 계약으로 Python dataclass로 정의",
    "BuildManifest는 실행별 1건 생성되는 결과 기록",
    "관계형 스키마가 아니므로 UML 클래스 다이어그램 표기법으로 정리",
])))
parts.append(sheet("엔티티 관계도 - 저장 구조 (ERD)", fig("storage.svg", "SQLite 저장 구조 ERD", "mid") + ul([
    "상태 정보는 SQLite와 로컬 파일에 보관",
    "<code>builds</code>는 manifest.json과 종료 기록으로부터 재구성 가능한 파생 인덱스",
    "<code>tables</code>·<code>table_snapshots</code>는 웨어하우스 카탈로그, 스냅샷 본문은 Parquet 파일",
    "주요 컬럼만 표시",
])))

# ---------------------------------------------------------------- 기능 처리도
parts.append(sheet("기능 처리도 - 테이블 만들기", fig("flow-create.svg", "테이블 만들기 처리도", "tall") + ul([
    "사용자 조작(①⑦)은 Studio 내부에서 처리, Builder API 호출 지점은 미리보기·검증·존재 확인·제출 4곳",
    "미리보기·검증 동시 요청, 지연 도착한 이전 응답은 폐기",
    "제출 직전 동일 이름 테이블 존재 여부 재확인, 결과 변경 시 제출 중단",
    "제출 수락 즉시 실행 상세로 이동하며 진행 상황은 실행 상세에서 조회",
])))
parts.append(sheet("기능 처리도 - 실행 검토·재실행", fig("flow-rerun.svg", "실행 검토와 재실행 처리도", "tall") + ul([
    "실행 상세는 단계·품질·이벤트·명세를 개별 조회하여 일부 실패가 전체 표시에 영향을 주지 않도록 구성",
    "실패·취소된 실행의 재실행 시에만 <code>retry_of</code> 전달, 수집 체크포인트 승계",
    "성공한 실행의 재실행은 갱신으로 처리되어 신규 스냅샷 생성",
])))
parts.append(sheet("기능 처리도 - 게시", fig("flow-publish.svg", "게시 처리도", "tall") + ul([
    "게시 전 준비 상태 조회로 라이선스, 개인정보 검사, 카드 누락 등 차단 사유 우선 표시",
    "Studio의 게시 대상은 Hugging Face, Builder CLI는 로컬·Kaggle 게시 추가 지원",
    "게시 요청은 자동 재시도 대상에서 제외, 결과 불명확 시 대조 또는 영수증 초기화로 복구",
])))
parts.append(sheet("기능 처리도 - 오류 처리", fig("flow-error.svg", "오류 처리 흐름") + ul([
    "① 명세 검증 오류: 문제 목록 표시, 수정 전까지 실행 차단",
    "② 연결 실패: 30초 제한, 최대 2회 재시도 후 오류 상태와 다시 시도 버튼 표시 (미리보기·제출·게시·쿼리는 재시도 제외)",
    "③ 인증 만료: 토큰 갱신 후 동일 요청 1회 재전송, 실패 시 로그인 화면 이동",
    "④ 실행 실패: 실행 상세에서 실패 단계·코드 확인 후 명세 수정 및 재실행",
    "오프라인 모드·자동 재연결 기능은 미제공. 주기적 조회 재개 시 화면 갱신",
])))
parts.append(sheet("기능 처리도 - Ask KPubData 응답 처리", fig("flow-assistant.svg", "AI 응답 처리 흐름") + ul([
    "프롬프트 역할 분리: 고정 지시(system), 비신뢰 근거(evidence), 사용자 질문을 구분하여 전달",
    "전송 전 비밀값 제거: 키·토큰 이름의 필드, <code>key=value</code> 형태, 무작위성이 높은 긴 문자열을 자리표시자로 치환",
    "4단계 검증: ① Zod 구조 검증 → ② 근거 대조 → ③ Builder 검증 → ④ 사용자 승인",
    "SQL 안전성 검사는 Builder의 읽기 전용 검사에서 수행 (Studio는 미수행)",
    "허용 동작 6종: OPEN_PROVIDER, OPEN_BUILD, OPEN_QUALITY, PATCH_BUILDSPEC, CREATE_BUILD_DRAFT, ADD_REPORT_BLOCK",
    "실행 시작, 게시, 자격 증명 변경, SQL 자동 실행은 제안 대상에서 제외",
    "LLM 키는 사용자 직접 입력(BYOK) 방식, 기본 메모리 보관",
])))

parts += detail.state_sheets()

# ---------------------------------------------------------------- 알고리즘 명세서
parts.append(sheet("알고리즘 명세서", fig("algorithm.svg", "run_build 알고리즘", "tall")))
parts.append(sheet("알고리즘 명세서", ul([
    "① <code>run_build()</code>가 BuildSpec을 입력받아 <code>validate_spec()</code>으로 사전 검증. 위반 시 <code>ValidationError</code>로 종료하며 작업공간·기록 미생성",
    "② <code>BuildContext.create()</code>로 실행 작업공간 생성, 명세 스냅샷(buildspec.yaml)과 <code>spec_digest</code> 기록",
    "③ 소스를 스레드 풀로 병렬 실행 (최대 4개). 결과는 명세 기재 순서대로 병합",
    "④ 소스별 Bronze → Silver → Gold → Export 순 진행. 단계 경계마다 취소 여부 확인",
    "⑤ Silver에서 스키마 검증, 개인정보 검사, 품질 검사 통과 시 Gold 진행",
    "⑥ composition 선언 시 두 소스의 Silver를 조인하여 단일 Gold 생성",
    "⑦ 상태 판정: 취소 시 cancelled, 오류 1건 이상 시 failed, 그 외 ok",
    "⑧ 상태가 ok인 경우에 한해 Gold를 웨어하우스 스냅샷으로 커밋. 시작 시점 revision과 비교하여 충돌 시 거부",
    "⑨ manifest.json 기록 후 <code>BuildResult(status, outcomes, manifest_path, …)</code> 반환",
]) + "<h3>상태값</h3>" + table(["계층", "값", "비고"], [
    [c("오케스트레이터·Manifest"), "<code>ok</code> · <code>failed</code> · <code>cancelled</code>", "실행 결과의 원본 값"],
    [c("HTTP API 작업 상태"), "<code>queued</code> · <code>running</code> · <code>cancelling</code> · <code>succeeded</code> · <code>failed</code> · <code>cancelled</code>", "<code>ok</code>는 <code>succeeded</code>로 표시. 테이블 커밋이 실패하면 <code>failed</code>"],
    [c("품질 검사"), "<code>pass</code> · <code>warn</code> · <code>fail</code>", "미평가 규칙은 결과에서 제외"],
], "small", ["42mm", None, "60mm"]) + "<h3>Manifest가 남지 않는 경우</h3>" + ul([
    "명세 검증에서 거부된 요청: 실행 미시작",
    "대기 중 취소, 서버 재시작 등으로 파이프라인 진입 전 종료된 비동기 실행: <code>run_endings</code> 표에 종료 기록 보관",
    "파이프라인 진입 후 취소된 실행은 <code>status=cancelled</code>, <code>partial=true</code>로 Manifest 기록",
])))

parts += detail.algorithm_detail_sheets()

# ---------------------------------------------------------------- 데이터 수집처리 정의서
parts.append(sheet("데이터 수집처리 정의서", "<p>○ Medallion 구조 기반 수집·처리 — Bronze / Silver / Gold 3단계 + Export</p>" + fig("pipeline.svg", "데이터 수집·처리 흐름", "low") + table(["단계", "처리 내용", "사용 기술", "입력 → 출력"], [
    [c("Bronze<br>(원천 수집)"), "공공 API·업로드 파일·URL의 원본을 변형 없이 수집. 수집 시각·파라미터·건수·체크섬 기록. 파라미터 조합별 체크포인트", "kpubdata, URL 수집기", "외부 원본 → <code>bronze/{source}/raw_records.jsonl</code>, <code>metadata.json</code>"],
    [c("Silver<br>(정제·검증)"), "명세에 선언한 규칙에 한해 적용: 결측 토큰 → 컬럼 병합 → 이름 변경 → 자리 채움 → 형 변환 → 파생 컬럼. 필수 컬럼·자료형 검증, 통계·미리보기 생성, 개인정보·품질 검사", "DuckDB", "Bronze → <code>silver/{source}/table.parquet</code>, <code>schema.json</code>, <code>stats.json</code>, <code>validation.json</code>"],
    [c("Gold<br>(패키징)"), "행 필터와 컬럼 선택, 선언한 개인정보 컬럼 마스킹, 분할, 두 소스 조인", "DuckDB", "Silver → <code>gold/{name}/table.parquet</code>, <code>package.json</code>, <code>splits/*.parquet</code>"],
    [c("Export<br>(내보내기)"), "Gold를 exports 설정에 맞춰 파일로 저장하고 데이터셋 카드 생성", "Exporter 6종 (csv, jsonl, parquet, markdown, huggingface, kaggle)", "Gold → 산출물 파일, <code>README.md</code>, <code>card.json</code>"],
    [c("웨어하우스 커밋"), "상태가 ok인 실행의 Gold를 읽기 전용 스냅샷으로 커밋. 최근 3개 유지", "SQLite 카탈로그, Parquet", "Gold → <code>tables/{id}/snapshots/{id}/</code>"],
], "small fixed", ["20mm", "62mm", "34mm", None]) + ul([
    "주요 선언 항목: 수집 파라미터(params·param_grid), 정규화 규칙(schema), 품질 기준(quality), 분할(splits), 내보내기(exports)",
    "Silver는 행·컬럼 전체 보존, 선택·필터는 Gold에서 수행",
])))

parts += detail.collection_detail_sheets()

# ---------------------------------------------------------------- 프로그램 목록 · 테이블 정의서
parts += detail.program_sheets()
parts += detail.table_sheets()

# ---------------------------------------------------------------- 핵심 소스코드
code1 = '''def run_build(spec: BuildSpec, *, client: SourceClient, output_root: Path,
              run_id: str | None = None, retry_of: str | None = None,
              catalog: TableCatalog | None = None, ...) -> BuildResult:
    validate_spec(spec)                                  # 위반 시 ValidationError, 기록 미생성
    context = BuildContext.create(spec, output_root=output_root, run_id=run_id)
    ...
    # Per-source fetch/stage mostly waits on network I/O, so concurrent
    # execution via thread pool reduces total time (#247). executor.map
    # returns results in spec.sources order, not completion order, so
    # downstream merge (manifest) stays deterministic.
    max_workers = min(len(spec.sources), _MAX_PARALLEL_SOURCES)
    clear_temp_root(context.output_root / context.run_id)
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(_worker, spec.sources))
    ...
    if cancelled:
        status = "cancelled"
    elif errors:
        status = "failed"
        recorder.run_failed(failed_source_count=len(errors))
    else:
        status = "ok"
        recorder.run_finished()
    ...                                                  # ok일 때 웨어하우스 커밋, manifest.json 기록'''
code2 = '''def validate_spec(spec: BuildSpec) -> None:
    """Validate BuildSpec minimum executability.

    Raises:
        ValidationError: When one or more validation rules fail.
    """
    problems: list[ValidationProblem] = []
    if not spec.dataset_id.strip():
        problems.append(_p("empty_field", "dataset_id", "dataset_id must be a non-empty string"))
    if not spec.title.strip():
        problems.append(_p("empty_field", "title", "title must be a non-empty string"))
    if not spec.description.strip():
        problems.append(_p("empty_field", "description", "description must be a non-empty string"))
    if not spec.sources:
        problems.append(_p("missing_sources", "sources", "at least one source is required"))
    ...
    # exports may be empty (#703). A build with none ends at a committed table,
    # which is a complete job — publishing is an explicit follow-up, not the only
    # way to finish.
    ...
    problems.extend(_split_problems(spec))
    problems.extend(_schema_problems(spec))
    problems.extend(_source_kind_problems(spec))
    problems.extend(_source_key_problems(spec))
    problems.extend(_param_grid_problems(spec))
    problems.extend(_pii_problems(spec))
    problems.extend(_license_problems(spec))
    problems.extend(_quality_problems(spec))
    problems.extend(_composition_problems(spec))
    problems.extend(_gold_selection_problems(spec))
    if problems:
        raise ValidationError([str(p) for p in problems], structured=problems)'''
code3 = '''export function crossCheckAssistantResponse(
  response: AssistantStructuredResponse,
  evidence: AssistantEvidence,
  knownRefs: AssistantKnownRefs,
): CrossCheckResult {
  const rejectedRefs: string[] = [];
  const evidenceRefs = response.evidenceRefs.filter((ref) => {
    const known = isKnownEvidenceRef(ref, knownRefs, evidence);
    if (!known) rejectedRefs.push(`${ref.kind}:${ref.id} (${ref.label})`);
    return known;
  });

  const rejectedActions: string[] = [];
  const suggestedActions = response.suggestedActions.filter((action) => {
    const check = isKnownAction(action, knownRefs, evidence);
    if (!check.ok) rejectedActions.push(check.reason);
    return check.ok;
  });

  let generatedSql = response.generatedSql;
  let rejectedSqlReason: string | undefined;
  if (generatedSql) {
    if (evidence.context.stage !== generatedSql.stage) {
      rejectedSqlReason = t("sqlStageMismatch", { ... });
      generatedSql = null;
    } else if (generatedSql.source && !knownRefs.sourceKeys.has(generatedSql.source)) {
      ...                                                // 소스가 하나면 소스 지정만 제거, 여럿이면 SQL 폐기
    }
  }
  ...
}'''
parts.append(sheet("핵심 소스코드(1) — kpubdata-builder · run_build()", f"<pre>{html.escape(code1)}</pre>" + ul([
    "BuildSpec 검증 후 실행 작업공간을 생성하고 소스별 Bronze→Silver→Gold 파이프라인을 병렬 실행하여 상태를 판정하는 핵심 로직",
    "결과를 명세 순서대로 병합하여 Manifest 기록 순서의 일관성 확보",
    "<code>...</code>은 생략 부분. 원본: <code>src/kpubdata_builder/pipeline/orchestrator.py</code>",
])))
parts.append(sheet("핵심 소스코드(2) — kpubdata-builder · validate_spec()", f"<pre>{html.escape(code2)}</pre>" + ul([
    "실행 자원 생성 전 명세의 문제를 일괄 수집·반환하는 사전 검증 로직",
    "반환값 없음. 문제 발견 시 code·path·message·hint를 포함한 <code>ValidationError</code> 발생",
    "<code>exports</code>는 생략 가능하며, 이 경우 테이블 커밋까지 수행",
    "<code>...</code>은 생략 부분. 원본: <code>src/kpubdata_builder/spec/validator.py</code>",
])))
parts.append(sheet("핵심 소스코드(3) — kpubdata-studio · 근거 대조", f"<pre>{html.escape(code3)}</pre>" + ul([
    "LLM 답변이 인용한 근거·제안 동작·SQL을 Builder 제공 근거와 대조하는 로직",
    "근거 미확인 항목만 제거하고 나머지 답변은 유지",
    "SQL은 현재 단계·소스와 불일치 시 폐기, 실행 전 최종 검사는 Builder에서 수행",
    "<code>...</code>은 생략 부분. 원본: <code>src/features/assistant/crossCheck.ts</code>",
])))


code4 = '''def validate_read_only_sql(sql: str) -> ValidatedSql:
    ...
    expression = statements[0]
    if not isinstance(expression, exp.Query):
        raise UnsafeQueryError("only SELECT queries are allowed")

    for with_node in expression.find_all(exp.With):
        if with_node.args.get("recursive"):
            raise UnsafeQueryError("recursive CTEs are not allowed")
        for cte in with_node.expressions:
            if cte.alias.casefold() == "dataset":
                raise UnsafeQueryError("CTE alias must not shadow dataset")

    _reject_unsupported_relations(cast(exp.Expression, expression))
    _reject_unsafe_functions(cast(exp.Expression, expression))
    root_scope = build_scope(expression)
    if root_scope is None:
        raise UnsafeQueryError("query scope could not be validated")

    for scope in root_scope.traverse():
        _validate_scope(scope)
    if _reachable_dataset_refs(root_scope) == 0:
        raise UnsafeQueryError("query must reference the logical dataset table")

    canonical = expression.copy()
    for node in canonical.walk():
        node.comments = []
    return ValidatedSql(canonical.sql(dialect="duckdb", pretty=False))'''
parts.append(sheet("핵심 소스코드(4) — kpubdata-builder · 읽기 전용 SQL 검사", f"<pre>{html.escape(code4)}</pre>" + ul([
    "사용자·AI 도우미가 전달한 SQL의 실행 전 검사 로직",
    "SELECT 단일 문장만 허용, 비허용 관계·함수 거부, 논리 테이블 <code>dataset</code> 참조 여부 확인",
    "통과한 문장은 주석을 제거한 표준형으로 재생성하여 반환, 실행에는 표준형만 사용",
    "<code>...</code>은 생략 부분. 원본: <code>src/kpubdata_builder/query/security.py</code>",
])))

parts += detail.test_deploy_sheets()

# ---------------------------------------------------------------- 참고
parts.append(sheet("참고", ul([
    f'KPubData Builder 기준 코드: <a href="{BUILDER}/ARCHITECTURE.md">0539bca</a> (2026-10-12, API 계약 1.123.0)',
    f'KPubData Studio 기준 코드: <a href="{STUDIO}/docs/INFORMATION_ARCHITECTURE.md">08e3e8a</a> (2026-10-12, 버전 0.4.0)',
    '화면 그림은 Studio 데모 모드 실행 화면을 캡처한 것으로, 표시 값은 데모 데이터',
    '기술 설명별 코드 근거: <a href="evidence.md">근거 목록</a>',
    '2026. 09. 08 판 대비 변경 사항: <a href="design-update-notes.md">제작설계서 변경 내역</a>',
])))

doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SW개발/HW제작 설계서 — 공공데이터 AI 데이터셋 자동 표준화 및 검증 플랫폼 개발</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{''.join(parts)}
</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(doc)
print(len(doc), "bytes,", len(parts), "sections")
