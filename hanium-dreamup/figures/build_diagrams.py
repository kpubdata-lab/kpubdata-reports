"""구성도·처리 흐름·메뉴·알고리즘·도메인 모델 그림을 SVG로 만든다.

    python3 build_diagrams.py

격자에 맞춰 손으로 배치한 그림이다. 순서도(flow-*.mmd)와 저장 구조(storage.mmd)는
Mermaid로 그리며 mermaid-config.json의 색을 같이 쓴다.
"""
from pathlib import Path

HERE = Path(__file__).parent
FONT = "Apple SD Gothic Neo, Pretendard, Malgun Gothic, Noto Sans KR, sans-serif"
INK = "#16233f"
LINE = "#5b6880"
# 종류별 (채움, 테두리, 글자)
KIND = {
    "user": ("#16233f", "#16233f", "#ffffff"),
    "head": ("#2f55b5", "#2f55b5", "#ffffff"),
    "studio": ("#eaf0fc", "#2f55b5", INK),
    "builder": ("#e7f5f0", "#2e8b6f", "#12372c"),
    "store": ("#fff4dc", "#c98a1b", "#4a3506"),
    "ext": ("#f1f3f6", "#8a94a6", "#2c3442"),
    "bronze": ("#f7e4d4", "#b5713a", "#4e2c10"),
    "silver": ("#eceff3", "#7d8794", "#2c3442"),
    "gold": ("#fdf1c4", "#c49a17", "#4a3a06"),
    "bad": ("#fdecec", "#c94a4a", "#5a1a1a"),
    "ghost": ("#ffffff", "#8a94a6", "#2c3442"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.items = []

    def text(self, x, y, s, size=13, weight=400, fill=INK, anchor="middle", mono=False):
        fam = "Menlo, Consolas, monospace" if mono else FONT
        self.items.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'
        )

    def box(self, x, y, w, h, kind, title, lines=(), pill=False, dashed=False, title_size=13.5):
        fill, stroke, ink = KIND[kind]
        r = h / 2 if pill else 9
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.items.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}/>'
        )
        n = len(lines)
        line_h = 16
        top = y + h / 2 - (n * line_h) / 2 + 4.5
        self.text(x + w / 2, top, title, title_size, 700, ink)
        for i, s in enumerate(lines, 1):
            self.text(x + w / 2, top + i * line_h, s, 11.5, 400, ink)

    def group(self, x, y, w, h, label, label_dx=16):
        self.items.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#f7f9fc" stroke="#c9d2e0" stroke-width="1.2"/>'
        )
        self.text(x + label_dx, y + 22, label, 12.5, 700, "#3c4a63", "start")

    def arrow(self, pts, label=None, dashed=False, label_at=None, anchor="middle", color=LINE):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.items.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6"{dash} marker-end="url(#arrow)"/>'
        )
        if label:
            if label_at is None:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                label_at = ((x1 + x2) / 2, (y1 + y2) / 2 - 6)
            lx, ly = label_at
            wid = len(label) * 11.5 * 0.62 + 10
            x0 = lx - wid / 2 if anchor == "middle" else (lx - 4 if anchor == "start" else lx - wid + 4)
            self.items.append(f'<rect x="{x0}" y="{ly - 12}" width="{wid}" height="16" fill="#ffffff" opacity="0.92"/>')
            self.text(lx, ly, label, 11.5, 400, "#3c4a63", anchor)

    def line(self, pts, dashed=False):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.items.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.4"{dash}/>')

    def save(self, name):
        body = "\n".join(self.items)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
            f'role="img" aria-label="{esc(self.label)}">\n'
            f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker></defs>\n'
            f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>\n{body}\n</svg>\n'
        )
        (HERE / name).write_text(svg, encoding="utf-8")
        print(name, self.w, self.h)


# ------------------------------------------------------------------ 서비스 구성도
def architecture():
    s = Svg(900, 600, "서비스 구성도: 사용자는 Studio를 쓰고, Studio는 Builder API를 호출하며, Builder는 kpubdata로 원천을 받아 Bronze·Silver·Gold로 처리한다")
    c = [200, 370, 540, 710]
    w = 150
    s.box(20, 42, 110, 46, "user", "사용자", pill=True)
    s.box(180, 30, 700, 70, "studio", "KPubData Studio — 웹 작업공간",
          ["카탈로그 · 테이블 · SQL 작업 공간 · 리포트 · 갱신 이력 · 품질 · 모니터링"])
    s.arrow([(130, 65), (180, 65)])
    s.group(180, 150, 700, 320, "KPubData Builder — 실행 · 웨어하우스", label_dx=190)
    # 행 A
    s.box(c[0], 190, w, 56, "builder", "HTTP API")
    s.box(c[3], 190, w, 56, "store", "테이블 스냅샷", ["Parquet"])
    # 행 B
    s.box(c[0], 290, w, 64, "builder", "오케스트레이터", ["run_build"])
    s.box(c[1], 290, w, 64, "bronze", "Bronze", ["원천 스냅샷"])
    s.box(c[2], 290, w, 64, "silver", "Silver", ["DuckDB 정규화 · 검증"])
    s.box(c[3], 290, w, 64, "gold", "Gold", ["선택 · 분할 · 패키징"])
    # 행 C
    s.box(c[2], 395, w, 56, "store", "Manifest", ["SQLite 인덱스"])
    s.box(c[3], 395, w, 56, "builder", "Exporter · Publisher")
    # 행 D (Builder 밖)
    s.box(c[0], 520, w, 56, "ext", "공공데이터 API")
    s.box(c[1], 520, w, 56, "ext", "kpubdata", ["공공 API 접근 라이브러리"])
    s.box(c[3], 520, w, 56, "ext", "게시 대상", ["파일 · Hugging Face · Kaggle"], pill=False)
    # 화살표
    s.arrow([(275, 100), (275, 190)], "검증 · 실행 · 조회 요청", label_at=(285, 136), anchor="start")
    s.arrow([(275, 246), (275, 290)], "빌드 제출", label_at=(285, 272), anchor="start")
    s.arrow([(350, 322), (370, 322)])
    s.arrow([(520, 322), (540, 322)])
    s.arrow([(690, 322), (710, 322)])
    s.arrow([(785, 290), (785, 246)], "커밋", label_at=(795, 272), anchor="start")
    s.arrow([(350, 218), (710, 218)], "읽기 전용 SQL", dashed=True, label_at=(530, 212))
    s.arrow([(815, 354), (815, 395)])
    s.arrow([(750, 354), (750, 374), (615, 374), (615, 395)])
    s.arrow([(350, 548), (370, 548)])
    s.arrow([(445, 520), (445, 354)], "표준 레코드", label_at=(455, 440), anchor="start")
    s.arrow([(785, 451), (785, 520)])
    s.save("architecture.svg")


# ------------------------------------------------------------------ 데이터 수집·처리
def pipeline():
    s = Svg(1080, 300, "데이터 수집·처리 흐름: 소스에서 Bronze, Silver, Gold, Export로 이어지고 Gold는 웨어하우스 스냅샷과 manifest.json으로 기록된다")
    s.box(20, 82, 130, 60, "ext", "소스", ["공공 API · 파일 · URL"], pill=False)
    s.group(175, 30, 730, 250, "실행 작업공간  {output}/{run_id}/")
    xs = [195, 375, 555, 735]
    s.box(xs[0], 62, 150, 100, "bronze", "Bronze", ["raw_records.jsonl", "metadata.json"])
    s.box(xs[1], 62, 150, 100, "silver", "Silver", ["table.parquet", "schema · stats", "validation.json"])
    s.box(xs[2], 62, 150, 100, "gold", "Gold", ["table.parquet", "package.json", "splits/*.parquet"])
    s.box(xs[3], 62, 150, 100, "builder", "Export", ["CSV · JSONL · Parquet", "README.md", "card.json"])
    s.box(xs[2], 212, 150, 48, "store", "웨어하우스 스냅샷")
    s.box(xs[3], 212, 150, 48, "store", "manifest.json")
    s.box(930, 82, 130, 60, "ext", "게시", ["Hugging Face · Kaggle"])
    s.arrow([(150, 112), (195, 112)])
    for a in xs[:3]:
        s.arrow([(a + 150, 112), (a + 180, 112)])
    s.arrow([(885, 112), (930, 112)], "선택", dashed=True, label_at=(907, 104))
    s.arrow([(600, 162), (600, 212)], "상태 ok", label_at=(590, 192), anchor="end")
    s.arrow([(670, 162), (670, 187), (810, 187), (810, 212)])
    s.save("pipeline.svg")


# ------------------------------------------------------------------ 메뉴 구성도
def menu():
    s = Svg(900, 440, "메뉴 구성도: 홈, 데이터, 분석, 운영, 연결·설정 다섯 묶음과 각 메뉴의 경로")
    cols = [
        ("홈", [("홈", "/")], []),
        ("데이터", [("카탈로그", "/discover"), ("테이블", "/tables")],
         [("테이블 만들기", "/add"), ("테이블 상세", "/tables/:id")]),
        ("분석", [("SQL 작업 공간", "/sql"), ("저장된 분석", "/analyses"), ("작업대", "/workspace"), ("리포트", "/reports")], []),
        ("운영", [("갱신 이력", "/refresh-jobs"), ("품질", "/quality"), ("모니터링", "/monitoring"), ("관리 (관리자)", "/admin")],
         [("실행 상세 · 산출물 · 게시", "/refresh-jobs/:id")]),
        ("연결 · 설정", [("연결", "/connections"), ("설정", "/settings")], []),
    ]
    w, gap, x0 = 160, 20, 20
    s.box(350, 14, 200, 40, "user", "KPubData Studio", pill=True)
    s.line([(450, 54), (450, 70)])
    s.line([(x0 + w / 2, 70), (x0 + 4 * (w + gap) + w / 2, 70)])
    for i, (head, items, subs) in enumerate(cols):
        x = x0 + i * (w + gap)
        s.arrow([(x + w / 2, 70), (x + w / 2, 88)])
        s.box(x, 88, w, 36, "head", head)
        y = 136
        for name, path in items:
            s.box(x, y, w, 46, "studio", name)
            s.items.pop()  # 제목만 다시 배치
            s.text(x + w / 2, y + 20, name, 13.5, 700, INK)
            s.text(x + w / 2, y + 36, path, 11, 400, "#3c4a63", mono=True)
            y += 56
        for name, path in subs:
            s.box(x + 12, y, w - 12, 46, "ghost", name, dashed=True)
            s.items.pop()
            s.text(x + 12 + (w - 12) / 2, y + 20, name, 12.5, 700, "#2c3442")
            s.text(x + 12 + (w - 12) / 2, y + 36, path, 10.5, 400, "#3c4a63", mono=True)
            y += 56
    # 범례
    s.items.append('<rect x="20" y="410" width="22" height="14" rx="4" fill="#eaf0fc" stroke="#2f55b5" stroke-width="1.2"/>')
    s.text(50, 421, "사이드바 메뉴", 11.5, 400, "#3c4a63", "start")
    s.items.append('<rect x="150" y="410" width="22" height="14" rx="4" fill="#ffffff" stroke="#8a94a6" stroke-width="1.2" stroke-dasharray="4 3"/>')
    s.text(180, 421, "메뉴에서 이어지는 화면", 11.5, 400, "#3c4a63", "start")
    s.save("menu.svg")


# ------------------------------------------------------------------ 알고리즘
def algorithm():
    s = Svg(900, 730, "run_build 알고리즘: 명세 검증, 작업공간 생성, 소스별 병렬 실행, 병합, 조인, 상태 판정, 스냅샷 커밋, Manifest 기록 순서")
    mx, mw = 340, 220          # 가운데 열
    lx, rx, sw = 40, 640, 220  # 왼쪽·오른쪽 열
    cx = mx + mw / 2
    s.box(mx + 30, 16, mw - 60, 40, "user", "run_build 시작", pill=True)
    s.box(mx, 84, mw, 50, "studio", "validate_spec", ["명세 사전 검증"])
    s.box(lx, 84, sw, 50, "bad", "ValidationError", ["기록 없이 종료"])
    s.box(mx, 166, mw, 50, "builder", "BuildContext 생성", ["명세 스냅샷 · spec_digest"])
    s.group(40, 246, 820, 122, "소스별 병렬 실행 · 최대 4개")
    xs = [60, 260, 460, 660]
    s.box(xs[0], 282, 180, 66, "bronze", "Bronze", ["수집 · 체크포인트"])
    s.box(xs[1], 282, 180, 66, "silver", "Silver", ["정규화 · 스키마 검증", "개인정보 · 품질 검사"])
    s.box(xs[2], 282, 180, 66, "gold", "Gold", ["선택 · 마스킹 · 분할"])
    s.box(xs[3], 282, 180, 66, "builder", "Export", ["파일 · 데이터셋 카드"])
    s.box(mx, 398, mw, 44, "builder", "결과 병합", ["명세에 적힌 순서 유지"])
    s.box(mx, 472, mw, 44, "studio", "composition 선언?")
    s.box(lx, 472, sw, 44, "gold", "두 Silver 조인 → Gold")
    s.box(mx, 546, mw, 44, "studio", "상태 판정", ["ok · failed · cancelled"])
    s.box(rx, 540, sw, 56, "store", "웨어하우스 스냅샷 커밋", ["revision 비교 · 최근 3개 유지"])
    s.box(mx, 620, mw, 44, "store", "manifest.json 기록")
    s.box(mx + 30, 690, mw - 60, 34, "user", "BuildResult 반환", pill=True)
    s.arrow([(cx, 56), (cx, 84)])
    s.arrow([(mx, 109), (lx + sw, 109)], "위반", label_at=(300, 103))
    s.arrow([(cx, 134), (cx, 166)], "통과", label_at=(cx + 10, 155), anchor="start")
    s.arrow([(cx, 216), (cx, 246)])
    for a in xs[:3]:
        s.arrow([(a + 180, 315), (a + 200, 315)])
    s.arrow([(cx, 368), (cx, 398)])
    s.arrow([(cx, 442), (cx, 472)])
    s.arrow([(mx, 494), (lx + sw, 494)], "예", label_at=(300, 488))
    s.arrow([(cx, 516), (cx, 546)], "아니오", label_at=(cx + 10, 536), anchor="start")
    s.arrow([(lx + sw / 2, 516), (lx + sw / 2, 568), (mx, 568)])
    s.arrow([(mx + mw, 568), (rx, 568)], "ok", label_at=(600, 562))
    s.arrow([(cx, 590), (cx, 620)], "failed · cancelled", label_at=(cx - 10, 610), anchor="end")
    s.arrow([(rx + sw / 2, 596), (rx + sw / 2, 642), (mx + mw, 642)])
    s.arrow([(cx, 664), (cx, 690)])
    s.save("algorithm.svg")


# ------------------------------------------------------------------ 도메인 모델
def entities():
    s = Svg(900, 720, "핵심 도메인 모델: BuildSpec이 SourceRef, ExportTarget, SplitSpec, QualityPolicy, PiiPolicy, CompositionSpec을 포함하고 실행마다 BuildManifest가 기록된다")
    ROW, HEAD = 18, 28

    def entity(x, y, w, name, rows, kind="head"):
        h = HEAD + len(rows) * ROW + 8
        fill = KIND[kind][1]
        s.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#ffffff" stroke="{fill}" stroke-width="1.4"/>')
        s.items.append(f'<path d="M{x},{y + HEAD} L{x},{y + 8} Q{x},{y} {x + 8},{y} L{x + w - 8},{y} Q{x + w},{y} {x + w},{y + 8} L{x + w},{y + HEAD} z" fill="{fill}"/>')
        s.text(x + w / 2, y + 19, name, 13, 700, "#ffffff")
        for i, (field, typ) in enumerate(rows):
            yy = y + HEAD + 15 + i * ROW
            if i % 2 == 1:
                s.items.append(f'<rect x="{x + 1}" y="{yy - 13}" width="{w - 2}" height="{ROW}" fill="#f4f7fc"/>')
            s.text(x + 10, yy, field, 11.5, 400, INK, "start", mono=True)
            s.text(x + w - 10, yy, typ, 11, 400, "#5b6880", "end")
        return h

    x1, x2, x3 = 20, 330, 640
    h_spec = entity(x1, 20, 250, "BuildSpec", [
        ("dataset_id", "str"), ("title", "str"), ("description", "str"), ("sources", "SourceRef[1..*]"),
        ("exports", "ExportTarget[0..*]"), ("splits", "SplitSpec?"), ("quality", "QualityPolicy?"),
        ("pii", "PiiPolicy?"), ("composition", "CompositionSpec?"), ("license", "str?"),
        ("publish", "bool"), ("refresh_cadence", "str?"),
    ])
    y_man = 20 + h_spec + 60
    entity(x1, y_man, 250, "BuildManifest", [
        ("build_id", "str"), ("status", "ok | failed | cancelled"), ("started_at / finished_at", "datetime"),
        ("inputs / outputs", "tuple"), ("row_counts", "dict"), ("provenance", "SourceProvenance[]"),
        ("quality_results", "dict"), ("failures", "RunFailure[]"), ("inputs_fingerprint", "str?"),
    ], "builder")
    # 가운데 열
    mids = []
    y = 20
    for name, rows, mult in [
        ("SourceRef", [("kind", "public_api | file | url"), ("provider / dataset", "str"), ("params", "dict"),
                       ("param_grid", "dict"), ("alias", "str"), ("schema", "SchemaContract?"), ("gold", "GoldSelection?")], "1..*"),
        ("ExportTarget", [("kind", "str"), ("output_path", "str"), ("options", "dict")], "0..*"),
        ("SplitSpec", [("mode", "ratio | key"), ("ratios", "dict"), ("key", "str"), ("seed", "int")], "0..1"),
        ("QualityPolicy", [("max_duplicate_rate", "float?"), ("max_null_ratio", "dict"), ("min_rows", "int?"), ("range", "RangeRule[]")], "0..1"),
        ("PiiPolicy", [("mode", "block | warn | allow"), ("allow_columns", "str[]")], "0..1"),
        ("CompositionSpec", [("name", "str"), ("join", "JoinSpec")], "0..1"),
    ]:
        h = entity(x2, y, 250, name, rows)
        mids.append((y + 14, mult))
        if name == "SourceRef":
            src_y = y
        y += h + 14
    # BuildSpec → 가운데 열
    trunk = 300
    s.line([(270, 60), (trunk, 60)])
    s.line([(trunk, mids[0][0]), (trunk, mids[-1][0])])
    for yy, mult in mids:
        s.arrow([(trunk, yy), (x2, yy)])
        s.text(x2 - 6, yy - 5, mult, 10.5, 400, "#3c4a63", "end")
    # 오른쪽 열
    hs = entity(x3, 20, 240, "SchemaContract", [
        ("required", "str[]"), ("dtypes", "dict"), ("casts", "dict"), ("rename", "dict"),
        ("derived", "DerivedColumn[]"), ("null_tokens", "str[]"), ("coalesce / zfill", "dict"),
    ])
    yg = 20 + hs + 14
    entity(x3, yg, 240, "GoldSelection", [("select", "str[]"), ("filters", "GoldFilter[]"), ("pii_columns", "str[]")])
    t2 = 610
    s.line([(580, src_y + 60), (t2, src_y + 60)])
    s.line([(t2, 34), (t2, yg + 14)])
    for yy in (34, yg + 14):
        s.arrow([(t2, yy), (x3, yy)])
        s.text(x3 - 6, yy - 5, "0..1", 10.5, 400, "#3c4a63", "end")
    # BuildSpec → Manifest
    s.arrow([(145, 20 + h_spec), (145, y_man)], "실행마다 1건 기록", dashed=True, label_at=(155, 20 + h_spec + 34), anchor="start")
    s.save("entities.svg")


if __name__ == "__main__":
    architecture()
    pipeline()
    menu()
    algorithm()
    entities()
