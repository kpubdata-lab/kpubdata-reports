// 시연 영상의 Studio 장면을 녹화한다. 실제 Builder(5199 → 8010)에 연결한 Studio와
// 데모 모드 Studio(5198, Ask KPubData 장면만)를 쓴다. Builder는 빈 상태에서 시작해야 한다.
//
//   NODE_PATH=<kpubdata-studio>/node_modules node record.cjs <out-dir> [scene ...]
//
// 장면마다 <out-dir>/<scene>.mp4와 <scene>.marks.json(동작 시각)을 남긴다.
const fs = require('fs');
const path = require('path');
const { launch } = require('./lib.cjs');

const REAL = 'http://localhost:5199';
const DEMO = 'http://localhost:5198';
const OUT = process.argv[2];
const ONLY = process.argv.slice(3);
const SPEC = fs.readFileSync(path.join(__dirname, 'apt-trade-gangnam.yaml'), 'utf8');
const SQL = `SELECT neighborhood, COUNT(*) AS deals,
       ROUND(AVG(deal_amount_10k_krw)) AS avg_price
FROM dataset
GROUP BY neighborhood
ORDER BY deals DESC
LIMIT 10`;

const state = {};

const scenes = {
  // D1: 카탈로그에서 아파트 실거래가를 찾아 시작한다.
  async 'rec-01-catalog'({ ui, page, recorder }) {
    await page.goto(`${REAL}/discover`, { waitUntil: 'networkidle' });
    await ui.sleep(800);
    await recorder.start(path.join(OUT, 'rec-01-catalog.mp4'));
    recorder.mark('search');
    await ui.type(page.getByPlaceholder('소스 데이터셋명·기관 검색'), '아파트', { delay: 160 });
    await ui.sleep(700);
    recorder.mark('row');
    const row = page.locator('tbody tr', { hasText: 'datago.apt_trade' });
    await ui.moveTo(row.locator('td').nth(4));
    await ui.sleep(900);
    recorder.mark('start');
    await ui.click(row.getByRole('button', { name: '시작' }));
    await page.locator('#add-data-param-LAWD_CD').waitFor();
    await ui.sleep(1200);
    recorder.mark('wizard');
    await recorder.stop();
  },

  // D2: 구성 단계에서 조회 조건을 입력한다.
  async 'rec-02-configure'({ ui, page, recorder }) {
    await recorder.start(path.join(OUT, 'rec-02-configure.mp4'));
    recorder.mark('steps');
    await ui.sleep(1200);
    await ui.moveTo(page.getByText('공공 API', { exact: true }));
    await ui.sleep(600);
    await ui.scroll(420);
    recorder.mark('lawd');
    await ui.type(page.locator('#add-data-param-LAWD_CD'), '11680', { delay: 140 });
    await ui.sleep(300);
    recorder.mark('ymd');
    await ui.type(page.locator('#add-data-param-DEAL_YMD'), '202409', { delay: 140 });
    await ui.sleep(1000);
    recorder.mark('end');
    await recorder.stop();

    // 녹화하지 않는 구간: 품질 규칙·개인정보 정책·라이선스·정규화 규칙을 YAML 편집 모드로 적용한다.
    await page.getByText('기준 BuildSpec', { exact: false }).click();
    await page.getByRole('button', { name: 'YAML', exact: true }).click();
    await page.locator('details textarea.font-mono').fill(SPEC);
    await page.getByRole('button', { name: 'YAML 적용' }).click();
    await ui.sleep(600);
    await page.getByRole('button', { name: '폼', exact: true }).click();
    await page.getByText('기준 BuildSpec', { exact: false }).click();
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await ui.sleep(500);
  },

  // D2·D3·R1·R2: 미리보기·검증 → 만들기 → 실행 상세에서 단계 진행과 품질 결과.
  async 'rec-03-preview-run'({ ui, page, recorder }) {
    await recorder.start(path.join(OUT, 'rec-03-preview-run.mp4'));
    recorder.mark('next1');
    await ui.click(page.getByRole('button', { name: '다음', exact: true }));
    await ui.sleep(700);
    recorder.mark('preview');
    await ui.click(page.getByRole('button', { name: '미리보기 새로고침' }));
    await page.getByText('검사 통과').waitFor({ timeout: 60000 });
    recorder.mark('previewDone');
    await ui.sleep(1500);
    await ui.scroll(380);
    recorder.mark('validation');
    await ui.moveTo(page.getByText('검사 통과'));
    await ui.sleep(1800);
    recorder.mark('next2');
    await ui.click(page.getByRole('button', { name: '다음', exact: true }));
    await ui.sleep(900);
    recorder.mark('review');
    await ui.moveTo(page.getByText('통과', { exact: true }).first());
    await ui.sleep(1600);
    recorder.mark('create');
    await ui.click(page.getByRole('button', { name: '테이블 만들기' }).last());
    await page.waitForURL(/refresh-jobs\//, { timeout: 30000 });
    recorder.mark('runPage');
    await page.getByText('모든 소스 성공').waitFor({ timeout: 120000 });
    recorder.mark('runDone');
    state.runId = page.url().match(/refresh-jobs\/([^/?]+)/)[1];
    await ui.sleep(1500);
    await ui.moveTo(page.getByText('224행 · 컬럼 9개'));
    await ui.sleep(1200);
    recorder.mark('quality');
    await ui.moveTo(page.getByText(/8\/8 PASS/));
    await ui.sleep(2200);
    recorder.mark('end');
    await recorder.stop();
  },

  // A1: 테이블 상세의 스냅샷.
  async 'rec-04-table'({ ui, page, recorder }) {
    await page.goto(`${REAL}/tables/datago-apt-trade`, { waitUntil: 'networkidle' });
    await ui.sleep(800);
    await recorder.start(path.join(OUT, 'rec-04-table.mp4'));
    recorder.mark('overview');
    await ui.moveTo(page.getByText('현재 스냅샷').first());
    await ui.sleep(1000);
    recorder.mark('tab');
    await ui.click(page.getByRole('tab', { name: '스냅샷' }));
    await ui.sleep(2500);
    recorder.mark('end');
    await recorder.stop();
  },

  // A2: SQL 작업 공간에서 스냅샷을 골라 질의하고 저장한 뒤, Builder 집계 차트를 그린다.
  async 'rec-05-sql'({ ui, page, recorder }) {
    await page.goto(`${REAL}/sql`, { waitUntil: 'networkidle' });
    await ui.sleep(800);
    await recorder.start(path.join(OUT, 'rec-05-sql.mp4'));
    recorder.mark('pick');
    await ui.click(page.getByText('apt_trade', { exact: true }));
    await ui.sleep(900);
    recorder.mark('type');
    await ui.click(page.locator('#sql-editor'));
    await page.keyboard.press('Control+A');
    await page.keyboard.type(SQL, { delay: 28 });
    await ui.sleep(400);
    recorder.mark('name');
    await ui.type(page.getByLabel('분석 이름'), '강남구 동별 거래량', { delay: 90 });
    recorder.mark('run');
    await ui.click(page.getByRole('button', { name: '실행하고 저장' }));
    await page.getByText(/전체 10행/).waitFor({ timeout: 30000 });
    recorder.mark('result');
    await ui.sleep(700);
    await page.getByText(/전체 10행/).evaluate((e) => e.scrollIntoView({ behavior: 'smooth', block: 'center' }));
    await ui.sleep(1800);
    recorder.mark('chart');
    await ui.click(page.getByRole('button', { name: '차트로 보기' }));
    await ui.sleep(1200);
    await page.locator('main svg').last().evaluate((e) => e.scrollIntoView({ behavior: 'smooth', block: 'center' }));
    await ui.sleep(1500);
    recorder.mark('chartDone');
    await ui.sleep(2500);
    recorder.mark('end');
    await recorder.stop();
  },

  // G2: 게시 준비 상태와 데이터 카드. 게시 버튼은 누르지 않는다.
  async 'rec-06-publish'({ ui, page, recorder }) {
    const runId = state.runId || process.env.RUN_ID;
    await page.goto(`${REAL}/refresh-jobs/${runId}/publish`, { waitUntil: 'networkidle' });
    await page.getByText('Builder 게시 준비 완료').waitFor({ timeout: 30000 });
    await ui.sleep(800);
    await recorder.start(path.join(OUT, 'rec-06-publish.mp4'));
    recorder.mark('ready');
    await ui.moveTo(page.getByText('Builder 게시 준비 완료'));
    await ui.sleep(1600);
    recorder.mark('card');
    await ui.scroll(560, { steps: 40 });
    await ui.sleep(1200);
    await ui.moveTo(page.getByText('개인정보', { exact: true }).last());
    await ui.sleep(1600);
    recorder.mark('end');
    await recorder.stop();
  },

  // G1: Ask KPubData (데모 모드 — Studio가 화면에 DEMO·mock 데이터라고 표시한다).
  async 'rec-07-assistant'({ ui, page, recorder }) {
    await page.goto(`${DEMO}/tables/apt-trade`, { waitUntil: 'networkidle' });
    await ui.sleep(800);
    await recorder.start(path.join(OUT, 'rec-07-assistant.mp4'));
    recorder.mark('open');
    await ui.click(page.getByRole('button', { name: /Ask KPubData/ }).first());
    await ui.sleep(900);
    recorder.mark('ask');
    await ui.type(page.getByPlaceholder(/질문을 입력하세요/), '이 테이블 상태를 알려 줘', { delay: 120 });
    await ui.click(page.getByRole('button', { name: '전송' }));
    await page.getByText('제안된 작업').waitFor({ timeout: 30000 });
    recorder.mark('answer');
    await ui.sleep(800);
    await ui.moveTo(page.getByText(/근거 \d+개/).first());
    await ui.sleep(1200);
    recorder.mark('approve');
    await ui.moveTo(page.getByRole('button', { name: '승인' }).first());
    await ui.sleep(1400);
    await ui.click(page.getByRole('button', { name: '승인' }).first());
    await ui.sleep(1500);
    recorder.mark('end');
    await recorder.stop();
  },
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const R = await launch();
  try {
    for (const [name, fn] of Object.entries(scenes)) {
      if (ONLY.length && !ONLY.includes(name)) continue;
      console.log('scene', name);
      await fn(R);
    }
    fs.writeFileSync(path.join(OUT, 'state.json'), JSON.stringify(state, null, 1) + '\n');
  } finally {
    if (R.recorder.proc && R.recorder.proc.exitCode === null) R.recorder.proc.kill('SIGINT');
    await R.close();
  }
})();
