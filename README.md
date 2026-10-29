# KPubData reports

KPubData Builder와 Studio에 관한 프로젝트 문서와 그 근거를 모아 둔 저장소입니다.

## 한이음 드림업 (26_HC277)

| 문서 | 보기 | 설명 |
|---|---|---|
| 프로젝트 결과보고서 | [HTML](hanium-dreamup/result-report.html) · [PDF](hanium-dreamup/result-report.pdf) | 제출 양식(서식4)의 순서와 표를 따른 초안 |
| SW개발/HW제작 설계서 | [HTML](hanium-dreamup/design-document.html) · [PDF](hanium-dreamup/design-document.pdf) | 2026. 09. 08 판을 현재 코드 기준으로 다시 쓴 개정판 |
| 근거 목록 | [evidence.md](hanium-dreamup/evidence.md) | 기준 커밋, 구현 사실과 출처, 검증 기록 |
| 제작설계서 변경 내역 | [design-update-notes.md](hanium-dreamup/design-update-notes.md) | 이전 판과 달라진 내용 |
| 시연 영상 | [video-storyboard.md](hanium-dreamup/video-storyboard.md) · [제작 파일](hanium-dreamup/video/) | 공모전 제출 영상(1:28, Full HD)의 설계·콘티와 녹화·내레이션·배경음·합성 스크립트. 내레이션 분량은 `video_narration_budget.py`로 검사 |

- 두 문서는 `hanium-dreamup/style.css`를 함께 씁니다. HTML은 생성 스크립트로 만듭니다: 결과보고서는 `build_report.py`, 제작설계서는 `build_design.py`(상세 절은 `design_detail.py`). 내용을 고칠 때는 스크립트를 고친 뒤 실행합니다. PDF는 Chrome 인쇄로 만든 것입니다.
- 그림은 `hanium-dreamup/figures/`에 있습니다. 구성도·처리 흐름·메뉴·알고리즘·도메인 모델은 `build_diagrams.py`로, 순서도와 저장 구조는 Mermaid(`*.mmd`, `mermaid-config.json`)로 만듭니다. 화면 캡처는 `figures/screens/`에 있습니다.
- 결과보고서의 노란색 표시는 팀에서 채워야 하는 항목입니다. 목록은 근거 목록의 "팀에서 채워야 하는 항목"에 있습니다.
- 화면 캡처는 데모 데이터로 실행한 Studio 화면입니다.

## PDF 다시 만들기

```sh
cd hanium-dreamup
python3 build_report.py && python3 build_design.py
chrome --headless=new --no-pdf-header-footer --print-to-pdf=result-report.pdf "file://$PWD/result-report.html"
chrome --headless=new --no-pdf-header-footer --print-to-pdf=design-document.pdf "file://$PWD/design-document.html"
```

## 시연 영상 다시 만들기

`hanium-dreamup/video-storyboard.md` §6(녹화)과 §9(합성)에 순서가 있습니다. 녹화 원본, 합성 음성, 배경음, 렌더 결과는 저장소에 넣지 않습니다(`hanium-dreamup/video/render/.gitignore`).

