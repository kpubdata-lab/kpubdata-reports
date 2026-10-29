# 시연 영상 만드는 법

한이음 드림업 공모전에 낸 KPubData 시연 영상(1분 29초, Full HD, 소리 없음, 자막 설명)을 **처음부터 다시 만들 수 있게** 정리한 안내입니다. 다른 프로젝트의 시연 영상을 만들 때도 같은 순서를 따라 하면 됩니다.

- 무엇을 보여 주는지(콘티, 자막, 원칙): [`../video-storyboard.md`](../video-storyboard.md)
- 완성본: 저장소 릴리스 `hanium-dreamup-video-*`의 첨부 파일

이 안내는 "왜 이렇게 했는지"도 함께 적습니다. 그대로 따라 하기보다, 각 단계에서 무엇을 정해야 하는지 익히는 데 쓰면 좋습니다.

## 목차

1. [전체 흐름](#1-전체-흐름)
2. [공고 조건부터 확인하기](#2-공고-조건부터-확인하기)
3. [준비물](#3-준비물)
4. [1단계: 기획](#4-1단계-기획)
5. [2단계: 콘티](#5-2단계-콘티)
6. [3단계: 녹화](#6-3단계-녹화)
7. [4단계: 자막](#7-4단계-자막)
8. [5단계: 합성](#8-5단계-합성)
9. [6단계: 렌더](#9-6단계-렌더)
10. [7단계: 검수](#10-7단계-검수)
11. [8단계: 유튜브 업로드와 제출](#11-8단계-유튜브-업로드와-제출)
12. [고치고 싶을 때 어디를 바꾸나](#12-고치고-싶을-때-어디를-바꾸나)
13. [이번에 실제로 겪은 문제](#13-이번에-실제로-겪은-문제)
14. [파일 구성과 도구](#14-파일-구성과-도구)

## 1. 전체 흐름

```text
공고 조건 확인 → 기획(메시지·순서) → 콘티(샷 표) → 녹화(실제 서비스 화면)
   → 자막 작성 → 합성(Remotion) → 렌더(mp4) → 검수 → 유튜브 업로드 → 링크 제출
```

| 단계 | 결과물 | 이 저장소의 파일 |
|---|---|---|
| 기획·콘티 | 샷 표, 자막 문장 | `../video-storyboard.md`, `captions.json` |
| 녹화 | 장면별 mp4와 동작 시각 | `rec/` |
| 합성 | 샷 배치, 확대, 자막, 그래픽 | `render/src/` |
| 렌더 | 제출용 mp4, 자막 srt, 썸네일 | `build-final.sh`, `make_srt.py` |

영상 편집 프로그램(Premiere, DaVinci Resolve, CapCut)으로도 같은 결과를 낼 수 있습니다. 이 저장소는 **코드로 편집**합니다. 다시 녹화해도 같은 동작이 나오고, 자막 하나를 고쳐도 명령 한 번으로 다시 만들 수 있기 때문입니다.

## 2. 공고 조건부터 확인하기

영상을 만들기 전에 공고문의 조건을 표로 옮겨 두고, 마지막 검수에서 다시 봅니다. 이번 공고의 조건과 이 영상의 대응입니다.

| 공고 조건 | 지키는 방법 |
|---|---|
| 유튜브 **일반 영상**(쇼츠 불인정), **공개**, 공모전 종료까지 유지 | 가로(16:9)로 만든다. 세로 영상은 쇼츠로 올라갈 수 있다 |
| **1분 30초 이내** | 콘티 단계에서 샷 길이 합을 89초로 맞춘다. 검사 스크립트가 90초를 넘으면 실패 |
| **HD급 이상** | 1920×1080으로 렌더한다 |
| **한국어** | 화면 문구와 자막을 한국어로 쓴다 |
| 프로젝트·주요 기능 설명은 **반드시 자막** | 설명을 모두 자막으로 쓰고 영상에 입힌다 |
| **음성·음향·BGM 사용 불가**(꼭 필요하면 시작에 자막으로 표시) | 오디오 트랙을 아예 만들지 않는다(`--muted`) |
| **블라인드 평가**: 학교명·팀원 실명 기재 금지 | 엔드 카드에 팀명·학교·GitHub 주소를 넣지 않는다. 화면에 계정·경로가 나오지 않게 녹화한다 |

> 처음에는 내레이션과 배경음을 넣었다가, 공고의 "음성/음향/BGM 사용 불가" 조건을 보고 모두 뺐습니다. **공고 PDF를 가장 먼저 읽으세요.**

## 3. 준비물

### 도구

| 도구 | 버전(이번에 쓴 것) | 쓰는 곳 |
|---|---|---|
| Node.js | 22 이상(24.14) | 녹화 스크립트, Remotion |
| Python | 3.10 이상 | 자막 검사, srt 생성, Builder |
| ffmpeg / ffprobe | 4.x 이상 | 녹화(x11grab), 파일 확인, 메타데이터 제거 |
| Google Chrome | 최신 | 녹화 브라우저 |
| Xvfb | 리눅스 패키지 `xvfb` | 화면 없이 크롬을 띄우는 가상 화면 |
| kpubdata-builder, kpubdata-studio | 각 저장소 `main` | 실제로 시연할 서비스 |

리눅스(우분투) 예:

```sh
sudo apt install ffmpeg xvfb x11-utils
# Google Chrome은 google.com/chrome에서 .deb를 받아 설치
```

> **macOS·Windows**: Xvfb와 x11grab은 리눅스 전용입니다. WSL2(우분투)에서 진행하거나, 녹화만 OBS Studio로 하고(1440×900 창, 30 fps) 나머지 단계는 그대로 따라 하면 됩니다.

### 서비스와 키

```sh
git clone https://github.com/kpubdata-lab/kpubdata-builder
git clone https://github.com/kpubdata-lab/kpubdata-studio
cd kpubdata-builder && uv sync && uv pip install xmltodict huggingface-hub
cd ../kpubdata-studio && npm ci
```

- `KPUBDATA_DATAGO_API_KEY`: [공공데이터포털](https://www.data.go.kr)에서 발급한 서비스 키. 아파트 매매 실거래가 API 활용 신청이 되어 있어야 합니다.
- `HF_TOKEN`: 게시 준비 상태 점검용(선택). 실제로 게시하지는 않습니다.

키는 환경변수로만 넣고 **파일에 적거나 커밋하지 않습니다.**

## 4. 1단계: 기획

1분 30초는 생각보다 짧습니다. 기능을 다 보여 주려 하지 말고 **보는 사람이 기억할 한 줄**부터 정합니다.

1. **한 줄 메시지**: "공공데이터를, 바로 쓰는 테이블로."
2. **보는 사람**: 심사위원. 1분 30초 안에 "무엇을 해결했고, 실제로 동작하는가"를 판단합니다.
3. **이야기 순서**: 문제 → 해결 방식 → 서비스 전체 → 한 사람이 처음부터 끝까지 쓰는 시연 → 정리
4. **시연 시나리오 하나**: 메뉴를 차례로 누르는 대신, 한 데이터(서울 강남구 아파트 실거래가)로 찾기 → 만들기 → 실행 → 분석 → 게시까지 이어 갑니다.
5. **뺄 것 정하기**: 넣고 싶은 기능이 많으면 결과보고서에 맡기고 영상에서는 뺍니다. 이번에는 작업대, 리포트, 설정, 테스트 결과를 뺐습니다.

> 처음 만든 판은 기능 화면을 크게 확대해 보여 줬더니 "서비스가 전체적으로 보이지 않는다"는 의견이 나왔습니다. 그래서 **서비스 둘러보기 장면(O1)**을 넣고, 화면을 원래 크기에 가깝게 보여 주도록 바꿨습니다. 확대는 꼭 필요한 곳에만 조금 씁니다.

## 5. 2단계: 콘티

콘티는 **샷 하나를 한 줄로** 적은 표입니다. [`../video-storyboard.md`](../video-storyboard.md) §3을 보세요.

| 열 | 적는 것 | 예 |
|---|---|---|
| 샷 | 이름(영문 1자 + 숫자) | `D2` |
| 시간 | 시작–끝 | `0:37–0:45` |
| 화면·움직임 | 무엇을 누르고 무엇이 나오는지 | 조회 조건 입력 → 미리보기 새로고침 → 샘플 행 |
| 화면 문구 | 창 위에 크게 쓸 요점 | 구성 → 미리보기·검증 → 만들기 |
| 소스 | 어느 녹화의 몇 초부터 몇 초까지 | `rec-03-preview-run 0.6–7.8초` |
| 자막 | 설명 문장 | 테이블은 3단계로 만듭니다… |

샷 길이는 **자막을 읽을 시간**으로 정합니다. 기준은 공백을 뺀 글자 수가 자막이 떠 있는 1초당 **9자 이하**입니다. 표를 고친 뒤에는 검사를 돌립니다.

```sh
python3 hanium-dreamup/video_caption_budget.py
```

이 스크립트는 샷이 끊김 없이 이어지는지, 전체가 90초를 넘지 않는지, 자막이 너무 빠르지 않은지, 표의 자막과 `captions.json`이 같은지 확인합니다. 하나라도 어긋나면 실패하므로, 콘티를 고칠 때마다 돌리면 됩니다.

## 6. 3단계: 녹화

### 6.1 무엇을 녹화하나

**실제로 동작하는 서비스**를 녹화합니다. 데모 데이터나 꾸민 화면을 쓰면 심사에서 신뢰를 잃습니다. 이번에는 로컬 Builder와 공공데이터포털 API로 강남구 2024년 9월 거래 224건을 실제로 처리했습니다. AI 도우미 장면만 LLM 키가 없어 데모 모드로 찍고, 화면에 "데모 모드"라고 표시했습니다.

### 6.2 녹화 방식

손으로 녹화하면 다시 찍을 때마다 동작이 달라집니다. 그래서 **Playwright 스크립트가 마우스와 키보드를 대신 움직이고, ffmpeg가 화면을 녹화**합니다.

| 파일 | 하는 일 |
|---|---|
| `rec/lib.cjs` | 가상 화면(Xvfb)과 크롬(키오스크 모드)을 띄우고, 부드러운 마우스 이동·클릭·타이핑, 녹화 시작·끝, 동작 시각 기록 |
| `rec/record.cjs` | 장면 8개의 동작 순서. 장면마다 `rec-XX.mp4`와 `rec-XX.marks.json`을 만든다 |
| `rec/serve-builder.sh` | 녹화용 Builder를 빈 상태로 띄운다 |
| `rec/record-all.sh` | Builder를 새로 띄우고 `record.cjs`를 실행한다 |
| `rec/apt-trade-gangnam.yaml` | 시연에 쓰는 BuildSpec(정규화·품질·개인정보·라이선스 규칙) |

녹화 설정의 이유:

- **1440×900, 배율 2**: 실제로는 2880×1800 픽셀로 녹화합니다. 영상에서 조금 확대해도 글자가 선명합니다.
- **키오스크 모드**: 탭, 주소창, 북마크가 안 보입니다. 주소창에 나올 수 있는 개인 정보도 막습니다.
- **그려 넣은 커서**: Playwright의 마우스는 진짜 마우스 포인터를 움직이지 않습니다. 그래서 페이지 안에 커서와 클릭 표시를 그립니다.
- **글꼴**: 리눅스에는 한글 기본 글꼴이 없어 Studio가 어색한 글꼴로 나옵니다. 녹화 브라우저에서만 Pretendard를 기본 글꼴로 지정합니다. 화면 내용은 바꾸지 않습니다.

### 6.3 녹화하기

터미널 세 개를 씁니다.

```sh
# 터미널 1: 실제 Builder와 연결한 Studio
cd kpubdata-studio
VITE_USE_REAL_BUILDER=true VITE_BUILDER_API_URL=http://localhost:8010 VITE_DEV_BYPASS_AUTH=true npx vite --port 5199

# 터미널 2: 데모 모드 Studio (AI 도우미 장면용)
cd kpubdata-studio
VITE_USE_REAL_BUILDER=false npx vite --port 5198

# 터미널 3: 녹화 (Builder는 스크립트가 새로 띄운다)
export KPUBDATA_DATAGO_API_KEY=...   HF_TOKEN=...
BUILDER_DIR=$PWD/kpubdata-builder STUDIO_DIR=$PWD/kpubdata-studio \
  bash kpubdata-showcase/hanium-dreamup/video/rec/record-all.sh ~/video-rec
```

장면 몇 개만 다시 찍으려면 이름을 뒤에 붙입니다. 단, Builder가 빈 상태로 시작하므로 테이블이 필요한 장면 앞에는 테이블을 만드는 장면(01~03)도 같이 넣어야 합니다.

```sh
bash .../record-all.sh ~/video-rec rec-01-catalog rec-02-configure rec-03-preview-run rec-08-overview
```

### 6.4 녹화 확인

녹화가 끝나면 장면마다 동작 시각이 남습니다.

```json
[{"label": "search", "t": 0.7}, {"label": "start", "t": 4.4}, ...]
```

이 시각을 보고 콘티의 "소스" 열(몇 초부터 몇 초까지)을 정합니다. 프레임을 뽑아 눈으로도 확인합니다.

```sh
ffmpeg -ss 4.4 -i ~/video-rec/rec-01-catalog.mp4 -frames:v 1 check.png
```

### 6.5 장면을 새로 넣으려면

`record.cjs`의 `scenes`에 함수를 하나 더합니다.

```js
async 'rec-09-quality'({ ui, page, recorder }) {
  await page.goto(`${REAL}/quality`, { waitUntil: 'networkidle' });
  await recorder.start(path.join(OUT, 'rec-09-quality.mp4'));
  recorder.mark('open');
  await ui.click(page.getByText('이 문제 실행 보기'));
  await ui.sleep(2000);
  recorder.mark('end');
  await recorder.stop();
},
```

화면 요소는 **사람이 보는 글자**로 찾습니다(`getByText`, `getByRole('button', { name: '…' })`). 클래스 이름보다 덜 깨집니다.

## 7. 4단계: 자막

자막 문장은 [`captions.json`](captions.json)에 샷별로 하나씩 있습니다. 콘티 표의 자막 열과 같아야 합니다(검사 스크립트가 확인).

잘 읽히는 자막을 쓰는 요령:

- **한 샷에 한 문장, 정보 하나.** "~합니다"체로 씁니다.
- **화면 문구와 역할을 나눕니다.** 창 위의 화면 문구는 요점("실행 전에, 먼저 검증."), 아래 자막은 설명("명세 검증을 통과해야만 실행할 수 있습니다.")입니다.
- **화면에 보이는 것을 말합니다.** 자막이 말하는 버튼이나 숫자가 그 순간 화면에 있어야 합니다.
- **사실만 씁니다.** 자막의 주장마다 결과보고서나 코드의 근거가 있어야 합니다(콘티 §8).
- **영어 제품명은 그대로**(Builder, Studio, SQL) 두되, 설명은 한국어로 씁니다.

## 8. 5단계: 합성

합성은 [Remotion](https://www.remotion.dev)으로 합니다. React 컴포넌트로 화면을 그리고, 프레임 단위로 시간을 정해 mp4로 렌더하는 도구입니다.

```sh
cd hanium-dreamup/video/render
npm ci
mkdir -p public/footage && cp ~/video-rec/rec-0*.mp4 public/footage/
cp ../PretendardVariable.woff2 public/ && mkdir -p public/brand && cp ../symbol_light.svg public/brand/
npm run studio        # 브라우저에서 미리 보기(타임라인을 움직이며 확인)
```

### 8.1 `src/timeline.ts`: 무엇을 언제 보여 주나

샷 하나가 객체 하나입니다. 시간 단위는 **프레임**(30프레임 = 1초)입니다.

```ts
{
  id: 'D2', dur: 240, kind: 'proof',              // 8초짜리 녹화 화면 샷
  kicker: '02 · 만들기', heading: '구성 → 미리보기·검증 → 만들기',
  chip: REAL,                                     // "실제 Builder 연동" 표시
  segments: [                                     // 녹화의 어느 구간을 몇 배속으로
    {src: 'rec-02-configure.mp4', from: 0.8, to: 9.2, rate: 2.6},
    {src: 'rec-03-preview-run.mp4', from: 0.6, to: 7.8, rate: 2},
  ],
  camera: [                                       // 확대 위치(샷 안의 프레임, 배율, 화면 중심 x·y 0~1)
    {at: 0, z: 1.25, x: 0.5, y: 0.3},
    {at: 44, z: 1.45, x: 0.74, y: 0.6},
  ],
}
```

- `segments`의 길이 합(`(to - from) / rate × 30`)이 샷 길이보다 짧으면 마지막 화면을 멈춰 채웁니다. `hold`로 멈출 프레임 수를 직접 정할 수도 있습니다.
- 2배를 넘게 빨리 돌리면 창 오른쪽 위에 "×N"이 자동으로 나옵니다. 보는 사람에게 빨리 돌렸다는 사실을 숨기지 않기 위해서입니다.
- `ZOOM_DAMP = 0.4`는 `camera`의 확대를 40%만 반영합니다. 서비스 화면이 거의 다 보이게 하려고 넣었습니다. 1로 바꾸면 적은 배율 그대로 확대합니다.
- `kind`가 `title`·`problem1`·`brand`·`pipeline`·`recap`·`end`인 샷은 녹화 없이 그린 그래픽입니다.

### 8.2 `src/Video.tsx`: 어떻게 그리나

| 컴포넌트 | 화면 |
|---|---|
| `TitleCard` | 제목 카드(T1)와 엔드 카드(F2) |
| `Problem1`, `Problem2` | 문제 제기 그래픽 |
| `Brand`, `Pipeline` | Builder·Studio 소개, 처리 흐름 |
| `Proof` | 녹화 화면: 창 모형, 확대, 배속 표시, 화면 문구 |
| `Recap` | 정리 문구 |
| `Subtitle` | 아래쪽 자막 띠 |

색은 `src/theme.ts`에 KPubData Brand v2 값으로 모여 있습니다. 새 색을 직접 쓰지 말고 여기 있는 값을 씁니다.

### 8.3 정지 화면으로 확인하기

전체를 렌더하기 전에 주요 프레임만 뽑아 확인하면 시간을 아낍니다(전체 렌더는 이 컴퓨터에서 약 15분).

```sh
npx remotion still src/index.ts Main out/f1150.png --frame=1150
```

## 9. 6단계: 렌더

```sh
cd hanium-dreamup/video/render
bash ../build-final.sh            # 결과: out/final/
```

`build-final.sh`가 하는 일:

1. Remotion으로 1920×1080 30 fps mp4를 **소리 없이** 렌더합니다(`--muted`).
2. ffmpeg로 파일 메타데이터(작성자·제목 등)를 지웁니다. 블라인드 평가 대비입니다.
3. 같은 내용의 한국어 자막 `.srt`를 만듭니다(`make_srt.py`).
4. 1280×720 썸네일을 제목 카드로 만듭니다.

결과 확인:

```sh
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact out/final/kpubdata-dreamup-2026_1080p.mp4
# stream|codec_type=video|width=1920|height=1080|r_frame_rate=30/1   ← 오디오 줄이 없어야 함
# format|duration=89.0…                                             ← 90초 미만
```

## 10. 7단계: 검수

렌더한 영상을 **처음부터 끝까지 한 번은 0.5배속으로** 보면서 아래를 확인합니다.

**공고 조건**
- [ ] 90초 미만, 1920×1080, 가로 화면
- [ ] 소리가 없다(오디오 트랙 없음)
- [ ] 설명이 모두 자막으로 나온다

**블라인드 평가**
- [ ] 이름, 팀명, 과제 번호, 학교명, 학교 로고가 없다
- [ ] 화면에 이메일, GitHub·Hugging Face 계정, 컴퓨터 사용자명, 파일 경로가 없다
- [ ] 엔드 카드와 썸네일에도 없다

**정직성**
- [ ] 시연 화면은 실제 녹화이고, 결과 숫자를 고치지 않았다
- [ ] 데모 모드 장면에는 "데모 모드" 표시가 있다
- [ ] 2배 넘게 빨리 돌린 구간에 "×N" 표시가 있다
- [ ] 자막의 주장마다 근거가 있다(콘티 §8)

## 11. 8단계: 유튜브 업로드와 제출

1. 유튜브 스튜디오 → 만들기 → 동영상 업로드에서 `kpubdata-dreamup-2026_1080p.mp4`를 올립니다.
2. **제목·설명에 이름과 학교를 쓰지 않습니다.**
   - 제목 예: `2026 한이음 드림업 | 공공데이터 AI 데이터셋 자동 표준화 및 검증 플랫폼 개발 (KPubData)`
   - 설명 예: 프로젝트 한 줄 소개, 주요 기능 목록, "음성·음향 없이 자막으로 설명합니다."
3. 썸네일에 `kpubdata-dreamup-2026_thumbnail.png`를 올립니다.
4. 자막 → 업로드에서 `kpubdata-dreamup-2026.ko.srt`를 한국어 자막으로 올립니다(영상에도 이미 입혀져 있습니다).
5. "아동용 아님"을 고르고, 공개 범위를 **공개**로 합니다.
6. **채널 이름**에 실명이나 학교가 드러나는지 확인합니다. 드러나면 다른 채널을 씁니다.
7. 업로드 직후에는 SD 화질만 나옵니다. 몇 분 뒤 화질 메뉴에 **1080p**가 보이면 링크를 복사해 제출합니다.
8. 공모전이 끝날 때까지 영상을 지우거나 비공개로 바꾸지 않습니다.

## 12. 고치고 싶을 때 어디를 바꾸나

| 바꾸고 싶은 것 | 고칠 파일 | 다시 할 일 |
|---|---|---|
| 자막 문장 | `captions.json`, `../video-storyboard.md` 표 | 검사 → 렌더 |
| 화면 문구(창 위 한 줄) | `render/src/timeline.ts`의 `kicker`, `heading` | 렌더 |
| 샷 길이·순서 | `render/src/timeline.ts`, 콘티 표 | 검사 → 렌더 |
| 녹화 구간·배속 | `render/src/timeline.ts`의 `segments` | 렌더 |
| 확대 위치 | `render/src/timeline.ts`의 `camera`, `ZOOM_DAMP` | 정지 화면 확인 → 렌더 |
| 그래픽(문제 제기, 구성도, 엔드 카드) | `render/src/Video.tsx` | 렌더 |
| Studio에서 하는 동작 | `rec/record.cjs` | 녹화 → 구간 확인 → 렌더 |
| 시연 데이터(지역·기간·규칙) | `rec/apt-trade-gangnam.yaml`, `record.cjs`의 입력값 | 녹화 → 렌더 |

## 13. 이번에 실제로 겪은 문제

같은 문제를 만나면 아래를 먼저 보세요.

| 증상 | 원인 | 해결 |
|---|---|---|
| 미리보기가 "소스 조회에 실패했습니다" | 실거래가 API는 XML로 응답하는데 Builder 환경에 `xmltodict`가 없음 | `uv pip install xmltodict` (kpubdata의 `xml` extra) |
| 게시 준비 상태 점검이 안 됨 | `huggingface-hub` 패키지 없음 | `uv pip install huggingface-hub` |
| YAML을 적용하자 테이블 만들기 화면이 오류로 바뀜 | Studio가 YAML의 `metadata` 키와 `schema.required`·`dtypes`를 꼭 기대함 | 명세에 `metadata: {}`, `required: [...]`, `dtypes: {}`를 넣음 |
| 빌드가 Silver에서 실패, "PII 검출(name)" | 개인정보 `block` 정책의 컬럼 이름 규칙이 `NM`·`NAME`이 들어간 컬럼(`aptNm`, `roadNm`)을 잡음 | 그 컬럼들의 이름을 `rename`으로 바꿈(`apartment`, `road`…). 정책 자체는 유지 |
| 라이선스가 "카탈로그 선언과 다름" | 명세의 `license_name`이 카탈로그의 표기와 다름 | `license_name: 공공누리_1유형`으로 맞춤 |
| 두 번째 녹화부터 테이블 커밋 실패 | 같은 이름의 테이블이 이미 있음 | 녹화마다 빈 작업 디렉터리로 Builder를 새로 띄움(`record-all.sh`) |
| 크롬이 바로 죽음(`SIGTRAP`) | 프로필 경로가 길어 크롬 소켓 경로 길이 제한(약 107자)을 넘음 | 프로필을 짧은 `/tmp` 경로에 만들고 크롬에 `TMPDIR=/tmp`를 줌 |
| 탭·주소창·번역 팝업이 녹화됨 | 일반 브라우저 컨텍스트에는 `--kiosk`가 안 먹음 | `launchPersistentContext` + 번역 끈 프로필 |
| 녹화가 1초 남짓으로 짧음 | ffmpeg 인코딩이 화면 속도를 못 따라감 | `-preset ultrafast`, `-thread_queue_size 512` |
| 선택자 `getByText('GOLD')`가 못 찾음 | 화면에는 대문자지만 실제 글자는 `Gold`(CSS로 대문자 표시) | 화면에 보이는 다른 글자(`224행 · 컬럼 9개`)로 찾음 |
| 실패한 녹화 뒤 ffmpeg가 계속 돎 | 스크립트가 오류로 멈추면 녹화 종료가 안 불림 | `finally`에서 ffmpeg를 끝냄 |

## 14. 파일 구성과 도구

```text
hanium-dreamup/
├── video-storyboard.md        콘티와 원칙
├── video_caption_budget.py    콘티 검사(길이·자막 속도·captions.json 일치)
└── video/
    ├── README.md              이 안내
    ├── captions.json          자막 문장
    ├── title-card.html        제목 카드 시안(frames/T1.png)
    ├── symbol_light.svg       KPubData K 심볼(kpubdata-studio 브랜드 자산)
    ├── PretendardVariable.woff2, LICENSE-Pretendard.txt
    ├── build-final.sh         렌더 → 메타데이터 제거 → srt·썸네일
    ├── make_srt.py            타임라인과 자막으로 .srt 생성
    ├── rec/                   녹화 스크립트와 시연용 BuildSpec
    └── render/                Remotion 프로젝트(src/timeline.ts, src/Video.tsx, src/theme.ts)
```

녹화 원본(`render/public/footage/`)과 렌더 결과(`render/out/`)는 용량이 커서 저장소에 넣지 않습니다(`.gitignore`).

| 도구 | 라이선스 | 비고 |
|---|---|---|
| Playwright | Apache-2.0 | 녹화 자동화 |
| ffmpeg | LGPL/GPL | 녹화·확인 |
| Remotion | Remotion License(소스 공개) | 개인·3인 이하 회사·비영리는 무료. 팀 규모를 확인할 것 |
| Pretendard | SIL OFL 1.1 | 글꼴 |
| KPubData 브랜드 자산 | kpubdata-studio 저장소 | `docs/brand/VISUAL_IDENTITY.md`의 사용 규칙을 따름 |

이 방식은 CUBRID Lab 소개 영상의 제작 방식(`cubrid-lab/showcase`의 `projects/cubrid-lab/intro-video/`)을 참고했습니다.
