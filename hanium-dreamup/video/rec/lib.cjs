// 녹화 도구: Xvfb 화면에 크롬을 키오스크로 띄우고 ffmpeg x11grab으로 30fps 녹화한다.
// 화면은 1440×900 CSS 픽셀, 배율 2(2880×1800 픽셀)라서 영상에서 2배까지 확대해도 선명하다.
// 마우스는 X 커서가 아니라 페이지 안에 그린 커서다(Playwright 입력은 X 포인터를 움직이지 않는다).
const { chromium } = require('playwright');
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DISPLAY = process.env.REC_DISPLAY || ':99';
const W = 1440, H = 900, SCALE = 2;
const FONT = path.join(__dirname, '..', 'PretendardVariable.woff2');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// 녹화 머신(리눅스)에는 한글 시스템 글꼴이 없어 Studio가 WenQuanYi로 그려진다.
// 사용자 PC처럼 보이도록 Studio의 시스템 글꼴 자리에 Pretendard를 지정한다. 화면 내용은 바꾸지 않는다.
const INIT = `
(() => {
  const css = \`
    @font-face { font-family: "RecSans"; src: url("/__rec/font.woff2") format("woff2"); font-weight: 100 900; }
    :root { --font-sans: "RecSans", sans-serif !important; }
    html, body { font-family: "RecSans", sans-serif; }
    #__rec_cursor { position: fixed; left: 0; top: 0; width: 22px; height: 22px; z-index: 2147483647;
      pointer-events: none; transform: translate(-3px, -2px); transition: none; }
    #__rec_cursor.down svg { transform: scale(0.86); transform-origin: 3px 2px; }
    #__rec_ring { position: fixed; z-index: 2147483646; pointer-events: none; width: 36px; height: 36px;
      margin: -18px 0 0 -18px; border-radius: 50%; border: 3px solid rgba(37,99,235,0.55); opacity: 0; }
    #__rec_ring.on { animation: __rec_ring 420ms ease-out; }
    @keyframes __rec_ring { from { opacity: 1; transform: scale(0.4); } to { opacity: 0; transform: scale(1.4); } }
    ::-webkit-scrollbar { width: 0; height: 0; }
  \`;
  const add = () => {
    if (document.getElementById('__rec_style')) return;
    const s = document.createElement('style'); s.id = '__rec_style'; s.textContent = css;
    document.documentElement.appendChild(s);
    const c = document.createElement('div'); c.id = '__rec_cursor';
    c.innerHTML = '<svg width="22" height="22" viewBox="0 0 22 22"><path d="M3 2 L3 18 L7.5 14 L10.5 20.5 L13 19.4 L10.1 13 L16 13 Z" fill="#172033" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    document.documentElement.appendChild(c);
    const r = document.createElement('div'); r.id = '__rec_ring'; document.documentElement.appendChild(r);
    const pos = window.__recPos || { x: ${W / 2}, y: ${H / 2} };
    c.style.left = pos.x + 'px'; c.style.top = pos.y + 'px';
    window.addEventListener('mousemove', (e) => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; window.__recPos = { x: e.clientX, y: e.clientY }; }, true);
    window.addEventListener('mousedown', (e) => { c.classList.add('down'); r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px'; r.classList.remove('on'); void r.offsetWidth; r.classList.add('on'); }, true);
    window.addEventListener('mouseup', () => c.classList.remove('down'), true);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add();
})();
`;

function startDisplay() {
  if (spawnSync('xdpyinfo', ['-display', DISPLAY], { stdio: 'ignore' }).status === 0) return null;
  const x = spawn('Xvfb', [DISPLAY, '-screen', '0', `${W * SCALE}x${H * SCALE}x24`, '-nolisten', 'tcp'], { stdio: 'ignore' });
  return x;
}

async function launch() {
  const xvfb = startDisplay();
  await sleep(800);
  const killX = () => { if (xvfb) xvfb.kill(); };
  process.on('exit', killX);
  // 영구 프로필이어야 --kiosk가 첫 창에 적용된다. 번역 제안은 프로필 설정으로 끈다.
  // Chrome 단일 인스턴스 소켓은 경로 길이 제한(약 107자)이 있어 짧은 /tmp 경로를 쓴다.
  const profile = fs.mkdtempSync('/tmp/kpdrec-');
  fs.mkdirSync(path.join(profile, 'Default'), { recursive: true });
  fs.writeFileSync(path.join(profile, 'Default', 'Preferences'), JSON.stringify({
    translate: { enabled: false }, translate_blocked_languages: ['ko', 'en'],
    intl: { accept_languages: 'ko-KR,ko' }, browser: { has_seen_welcome_page: true },
  }));
  const context = await chromium.launchPersistentContext(profile, {
    channel: 'chrome',
    headless: false,
    viewport: null,
    locale: 'ko-KR',
    timezoneId: 'Asia/Seoul',
    env: { ...process.env, DISPLAY, TMPDIR: '/tmp' },
    ignoreDefaultArgs: ['--enable-automation'],
    args: ['--kiosk', `--force-device-scale-factor=${SCALE}`, '--window-position=0,0', `--window-size=${W},${H}`,
      '--disable-infobars', '--no-first-run', '--no-default-browser-check',
      '--disable-features=Translate,TranslateUI', '--lang=ko-KR'],
  });
  await context.route('**/__rec/font.woff2', (route) => route.fulfill({ path: FONT, contentType: 'font/woff2' }));
  await context.addInitScript(INIT);
  const page = context.pages()[0] || await context.newPage();
  page.on('pageerror', (e) => console.error('pageerror', e.message));
  let cursor = { x: W / 2, y: H / 2 };

  const ui = {
    page,
    async moveTo(target, { steps = 24, dx = 0, dy = 0 } = {}) {
      let x, y;
      if (typeof target.x === 'number') ({ x, y } = target);
      else {
        await target.scrollIntoViewIfNeeded();
        const b = await target.boundingBox();
        x = b.x + b.width / 2 + dx; y = b.y + b.height / 2 + dy;
      }
      // 처음과 끝이 느린 곡선으로 움직인다.
      const from = { ...cursor };
      for (let i = 1; i <= steps; i++) {
        const t = i / steps, e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        await page.mouse.move(from.x + (x - from.x) * e, from.y + (y - from.y) * e);
        await sleep(12);
      }
      cursor = { x, y };
    },
    async click(target, opts = {}) {
      await ui.moveTo(target, opts);
      await sleep(opts.before ?? 250);
      await page.mouse.down(); await sleep(90); await page.mouse.up();
      await sleep(opts.after ?? 350);
    },
    async type(target, text, { delay = 110 } = {}) {
      await ui.click(target);
      await page.keyboard.type(text, { delay });
    },
    async scroll(dy, { steps = 20 } = {}) {
      for (let i = 0; i < steps; i++) { await page.mouse.wheel(0, dy / steps); await sleep(16); }
      await sleep(300);
    },
    sleep,
  };

  const recorder = {
    proc: null, t0: 0, marks: [], name: '',
    async start(file) {
      this.name = file; this.marks = [];
      fs.mkdirSync(path.dirname(file), { recursive: true });
      this.proc = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-thread_queue_size', '512', '-f', 'x11grab', '-draw_mouse', '0', '-framerate', '30',
        '-video_size', `${W * SCALE}x${H * SCALE}`, '-i', `${DISPLAY}.0`, '-c:v', 'libx264', '-preset', 'ultrafast',
        '-crf', '14', '-pix_fmt', 'yuv420p', file], { stdio: ['pipe', 'inherit', 'inherit'] });
      this.t0 = Date.now();
      await sleep(700);
    },
    mark(label) { const t = (Date.now() - this.t0) / 1000; this.marks.push({ label, t }); console.log(`  mark ${label} @ ${t.toFixed(2)}s`); },
    async stop() {
      await sleep(500);
      const done = new Promise((r) => this.proc.on('exit', r));
      this.proc.stdin.write('q'); this.proc.stdin.end();
      await done;
      fs.writeFileSync(this.name.replace(/\.mp4$/, '.marks.json'), JSON.stringify(this.marks, null, 1) + '\n');
      console.log('saved', this.name);
    },
  };

  return {
    ui, recorder, page,
    async close() { await context.close(); if (xvfb) xvfb.kill(); },
  };
}

module.exports = { launch, sleep };
