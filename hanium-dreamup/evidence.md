# 근거 목록

결과보고서와 제작설계서에 쓴 기술 내용의 출처입니다. 본문에는 번호를 달지 않았고, 아래 "문서별 근거" 표로 대응시킵니다.

## 기준 자료

| 자료 | 기준 | 용도 |
|---|---|---|
| 한이음 드림업 결과보고서 양식 PDF | SHA-256 `e1d4287f9d1e0448add3a518a484300c8db861d890bee0f26e19429f41b48218` | 제출 양식 (본문은 비어 있음) |
| 한이음 제작설계서 PDF (2026. 09. 08) | SHA-256 `82201d9b1c35f34d434fba39466d9300cf83092620603b703574be7ec5263913` | 개정 전 설계서. 구성과 항목만 따르고 내용은 코드 기준으로 다시 씀 |
| Builder `main` | [`0539bca346e3f1fb046a5808a607559bfc0063bd`](https://github.com/kpubdata-lab/kpubdata-builder/tree/0539bca346e3f1fb046a5808a607559bfc0063bd) | 2026-10-12 19:20 KST 기준 최신 커밋 |
| Studio `main` | [`08e3e8aec189dfce14fdba7bb002b1a0167bc401`](https://github.com/kpubdata-lab/kpubdata-studio/tree/08e3e8aec189dfce14fdba7bb002b1a0167bc401) | 2026-10-12 18:59 KST 기준 최신 커밋 |

두 PDF 원본은 이 저장소에 넣지 않았습니다. 코드가 더 바뀌면 아래 내용을 다시 대조해야 합니다.

## 구현 사실과 출처

| ID | 사실 | 출처 |
|---|---|---|
| B-01 | Builder는 BuildSpec을 검증하고 Bronze → Silver → Gold를 실행하며 exporter와 publisher를 분리한다. | [아키텍처](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/ARCHITECTURE.md) |
| B-02 | 정식 실행 경로의 표 처리 엔진은 DuckDB이고 저장된 Parquet을 질의에 쓴다. `src/`는 Polars를 import하지 않는다. 레거시 게시 스크립트(`scripts/`)만 Polars를 쓴다. 전환 이유는 전체 데이터를 메모리에 올리는 구조의 한계(1,444 MiB 파일 소스 빌드 실패)다. | [아키텍처](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/ARCHITECTURE.md), [ADR 0021](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/docs/adrs/0021-duckdb-tabular-engine.md), [tabular 모듈](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/tabular) |
| B-03 | 상태값은 계층마다 다르다. 오케스트레이터와 Manifest는 `ok`·`failed`·`cancelled`, HTTP API 작업 상태는 `queued`·`running`·`cancelling`·`succeeded`·`failed`·`cancelled`다. 동기 빌드(`POST /build`)와 비동기 빌드(`POST /builds`)가 따로 있다. | [오케스트레이터](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/pipeline/orchestrator.py), [작업 상태](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/jobs.py), [빌드 상태 문서](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/docs/BUILD_STATE.md), [빌드 경로](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/routes/builds.py) |
| B-04 | `validate_spec(spec) -> None`은 15개 영역을 검사해 문제를 모은 뒤 `ValidationError`를 발생시킨다. `exports`는 비어 있어도 된다. 필수 항목은 `dataset_id`·`title`·`description`·`sources`다. | [검증기](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/spec/validator.py), [모델](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/spec/models.py), [로더](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/spec/loader.py) |
| B-05 | exporter는 csv·jsonl·parquet·markdown·huggingface·kaggle, publisher는 local·huggingface·kaggle이다. 게시 API는 준비 상태 점검·영수증·대조를 제공한다. | [exporter 등록](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/exporters/__init__.py), [publisher 등록](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/publishers/__init__.py), [API 계약](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/contract/builder-api.yaml) |
| B-06 | 상태는 SQLite와 로컬 파일에만 둔다. `builds` 인덱스는 Manifest와 종료 기록에서 다시 만들 수 있다. | [저장 백엔드](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/store/backend.py), [빌드 인덱스](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/store/build_index.py), [상태 목록](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/store/inventory.py) |
| B-07 | `run_build`는 소스를 스레드 풀로 병렬 실행한다(최대 4개). 상태가 ok일 때만 웨어하우스에 커밋하고(revision 비교, 최근 3개 유지) 그 뒤 manifest.json을 쓴다. | [오케스트레이터](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/pipeline/orchestrator.py) |
| B-08 | Manifest 필드와 `schema_version` 1.0.0. 파이프라인에 들어가기 전에 끝난 비동기 실행은 `run_endings` 표에 남는다. | [Manifest 모델](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/manifest/models.py), [이벤트 저장소](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/events/store.py) |
| B-09 | 소스 종류는 public_api·file·url이다. 파일은 csv·json·jsonl·parquet, URL은 HTTPS GET만 허용한다. | [모델](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/spec/models.py), [URL 수집](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/ingestion/url_fetch.py) |
| B-10 | 품질 규칙은 required_column·dtype·max_duplicate_rate·max_null_ratio·min_rows·range·compare_columns이고 결과는 pass·warn·fail이다. fail은 Gold 전에 소스를 중단한다. | [품질 평가](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/quality/evaluator.py) |
| B-11 | 개인정보 검사는 정규식(주민등록번호·전화번호·이메일·사업자번호)과 컬럼명 규칙 기반이다. 마스킹은 선언한 컬럼에 적용한다. 한국어 NER은 평가만 했다. | [검사](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/stages/silver/pii.py), [마스킹](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/stages/gold/pii.py), [NER 평가](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/docs/pii-korean-ner-evaluation.md) |
| B-12 | 재배포 판정은 kpubdata가 선언한 조건(allowed·non_commercial·forbidden·unknown) 중 가장 엄격한 값을 쓴다. 게시할 때 license가 필수다. | [재배포 판정](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/redistribution.py), [검증기](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/spec/validator.py) |
| B-13 | 읽기 전용 SQL 검사: 단일 SELECT, 재귀 CTE·테이블 함수·비결정 함수 금지, 논리 테이블 `dataset`만 참조. | [SQL 검사](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/query/security.py), [질의 서비스](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/query_service_api.py) |
| B-14 | 분할은 ratio(결정적 해시 정렬)와 key 두 방식이다. 데이터셋 카드는 README.md와 card.json으로 만든다. | [분할](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/stages/gold/split.py), [카드](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/stages/gold/card.py) |
| B-15 | 정기 수집은 GitHub Actions 일정(기상 3시간, 관광·DUR 주 1회, 부동산 월초)이 `publish-dataset.yml`을 호출하는 방식이며 레거시 게시 스크립트로 동작한다. 대기질은 수동 실행만 남아 있다. | [게시 워크플로](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/.github/workflows/publish-dataset.yml), [기상 일정](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/.github/workflows/scheduled-weather.yml) |
| B-16 | LLM 기반 스키마 매핑과 DVC는 코드에 없다. 버전 관리는 웨어하우스 스냅샷 revision과 명세 개정 이력으로 한다. | [웨어하우스 카탈로그](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/warehouse/catalog.py), [개정 이력](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/revisions.py) |
| B-17 | API 계약 버전은 1.123.0이다. CI는 ruff·mypy·pytest(Python 3.10~3.13)를 돌린다. | [계약 버전](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/src/kpubdata_builder/service/_contract_operations.py), [CI](https://github.com/kpubdata-lab/kpubdata-builder/blob/0539bca346e3f1fb046a5808a607559bfc0063bd/.github/workflows/ci.yml) |
| S-01 | 메뉴는 홈 / 데이터(카탈로그·테이블) / 분석(SQL 작업 공간·저장된 분석·작업대·리포트) / 운영(갱신 이력·품질·모니터링·관리) / 연결·설정이다. 이전 경로는 새 경로로 이동한다. | [레이아웃](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/app/Layout.tsx), [라우터](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/app/router.tsx), [정보 구조](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/docs/INFORMATION_ARCHITECTURE.md) |
| S-02 | 홈은 조치가 필요한 테이블, 최근 스냅샷, 최근 분석, 연결 문제를 보여 주고 첫 실행에는 체크리스트를 보여 준다. | [HomePage](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/pages/HomePage.tsx) |
| S-03 | 모니터링은 탭 없는 한 화면이며 30초 간격으로 조회하고 탭이 숨겨지면 멈춘다. | [MonitoringPage](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/pages/MonitoringPage.tsx) |
| S-04 | 리포트는 브라우저 localStorage에 저장하고 Markdown·HTML로 내려받는다. | [저장소](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/reports/repository.ts), [내보내기](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/reports/export.ts) |
| S-05 | 로그인은 Keycloak(OIDC Authorization Code + PKCE)으로 이동한다. 이메일·비밀번호 폼은 데모 모드에만 있다. | [LoginPage](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/pages/LoginPage.tsx), [keycloak](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/auth/keycloak.ts) |
| S-06 | AI 도우미의 이름은 Ask KPubData다. 응답은 Zod 구조 검증 → 근거 대조 → Builder 검증 → 사용자 승인 순으로 처리한다. Studio는 SQL을 직접 검사하지 않는다. 허용 동작은 6종이다. | [스키마](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/schema.ts), [근거 대조](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/crossCheck.ts), [질의](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/query.ts), [세션](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/useAssistantSession.ts) |
| S-07 | 화면 그림은 Studio를 데모 모드(`npm run dev`)로 실행해 1440×900으로 캡처했다. 표시된 값은 데모 데이터다. | [데모 모드](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/shared/lib/demoMode.ts) |
| S-08 | 테이블 만들기는 구성 → 미리보기·검증 → 만들기 3단계다. `/preview`와 `/validate`를 동시에 요청하고, 제출은 비동기 `POST /builds` 후 800ms 간격으로 상태를 조회한다. | [AddDataPage](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/pages/AddDataPage.tsx), [실행 API](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/runs/api/index.ts) |
| S-09 | 게시 화면의 대상은 Hugging Face다. 준비 상태 점검과 복구 패널이 있다. | [BuildPublishPage](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/pages/BuildPublishPage.tsx) |
| S-10 | API 클라이언트는 30초 제한과 최대 2회 재시도를 쓰고, 401에서는 토큰을 갱신해 한 번 다시 보낸다. 오프라인 모드는 없다. 최소 Builder 계약 버전은 1.96.0이다. | [builderApi](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/shared/lib/builderApi.ts), [인증 초기화](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/auth/init.ts) |
| S-11 | 스택: React 19.3, TypeScript 6, Vite 8, React Router 7, Zustand 5, Tailwind CSS 4, Zod 4, i18next(한국어·영어), keycloak-js, Vitest, Playwright. | [package.json](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/package.json) |
| S-12 | LLM 키는 기본적으로 메모리에만 두고, 사용자가 선택하면 localStorage에 저장한다. 전송 전에 비밀값을 자리표시자로 바꾼다. | [설정](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/config.ts), [비밀값 제거](https://github.com/kpubdata-lab/kpubdata-studio/blob/08e3e8aec189dfce14fdba7bb002b1a0167bc401/src/features/assistant/scrub.ts) |

## 문서별 근거

| 문서 위치 | 근거 |
|---|---|
| 결과보고서 Ⅰ. 개요, Ⅱ-1 구성도 / 설계서 서비스 구성도 | B-01, B-02, S-01 |
| 결과보고서 Ⅱ-2 기능, Ⅱ-3 적용 기술 / 설계서 요구사항 정의서 | B-04, B-05, B-09~B-16, S-01~S-10 |
| 결과보고서 Ⅱ-4 개발 환경 / 설계서 프로그램 목록 | B-17, S-11 |
| 결과보고서 Ⅲ-3 개발 측면 문제점 | B-02, B-03, B-07, B-08, S-01, S-06 |
| 설계서 서비스 흐름도, 기능 처리도 | B-03, S-08, S-09, S-10 |
| 설계서 메뉴 구성도, 화면 설계서 | S-01~S-09, S-12 |
| 설계서 엔티티 관계도, 테이블 정의서 | B-04, B-06, B-08 |
| 설계서 알고리즘 명세서, 데이터 수집처리 정의서 | B-01, B-02, B-07, B-10, B-11, B-14 |
| 설계서 핵심 소스코드 | B-04, B-07, S-06 |
| 설계서 시장 동향의 시장 규모·OECD 순위 | 코드 밖 자료. 제출 전 원문 확인 필요 |

## 팀에서 채워야 하는 항목

| 항목 | 필요한 자료 |
|---|---|
| 제출 연도 | 양식은 2025년, 제작설계서는 2026년으로 적혀 있음 |
| 참여자와 업무분장 | 팀에서 확정한 성명·역할 |
| 수행 일정 | 단계별 실제 기간, 멘토링·회의 기록 |
| 개발 장비·IDE·의사소통 도구·배포 환경 | 팀 자료 |
| 작동 동영상 | 유튜브 링크 |
| 달성 성과와 증빙 | 논문·등록·수상 등 접수증이나 공개 페이지 |
| 프로젝트 관리 측면의 문제점, 배우거나 느낀 점 | 참여자가 직접 작성 |
| 실제 운영 화면 | 현재 그림은 데모 데이터 화면 |

## 검증 기록 (2026-10-12)

| 대상 | 명령 | 결과 |
|---|---|---|
| Builder 구문 | `python3 -m compileall -q src/kpubdata_builder` | 종료 코드 0 |
| Builder 단위 테스트 | `uv run --locked pytest tests/unit/test_spec.py tests/unit/test_pipeline.py -q` | 실행하지 못함. `files.pythonhosted.org` 접속 오류로 의존성을 받지 못함 (두 번 시도) |
| Studio 테스트 | `npm test -- --run src/features/reports/repository.test.ts src/features/assistant/query.test.ts src/pages/HomePage.test.tsx` | 3개 파일, 37개 통과 |
| Studio 빌드 | `npm run build` | 성공, 번들 크기 기준 이내 |
| 화면 캡처 | Studio 데모 모드 실행 후 Playwright로 21개 화면 캡처 | 19개 사용. Ask KPubData 화면은 번역 키가 그대로 보여 제외, 관리 화면은 데모에서 내용이 없어 제외 |

Studio 테스트는 위 세 파일만 돌렸습니다. Builder는 구문 검사만 했고 동작 테스트는 하지 못했습니다.

## 다시 확인하는 방법

```sh
git clone https://github.com/kpubdata-lab/kpubdata-builder && git -C kpubdata-builder checkout 0539bca346e3f1fb046a5808a607559bfc0063bd
git clone https://github.com/kpubdata-lab/kpubdata-studio && git -C kpubdata-studio checkout 08e3e8aec189dfce14fdba7bb002b1a0167bc401
```
