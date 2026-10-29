import React from 'react';
import {
	AbsoluteFill,
	Freeze,
	Img,
	interpolate,
	OffthreadVideo,
	Sequence,
	staticFile,
	useCurrentFrame,
} from 'remotion';
import {C, MONO, SANS, ease} from './theme';
import {CAPTION_IN, CAPTION_OUT, Key, Segment, SHOTS, Shot, starts, ZOOM_DAMP} from './timeline';
import captions from '../../captions.json';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const fadeIn = (f: number, from: number, len = 10) => ease((f - from) / len);
const rise = (f: number, from: number, len = 12, dist = 24) => ({
	opacity: fadeIn(f, from, len),
	transform: `translateY(${(1 - fadeIn(f, from, len)) * dist}px)`,
});

const Symbol: React.FC<{size: number; style?: React.CSSProperties}> = ({size, style}) => (
	<Img src={staticFile('brand/symbol_light.svg')} style={{width: size, height: size, ...style}} />
);

/* ---------- T1 / F2: 제목 카드와 엔드 카드 (video/title-card.html과 같은 배치) ---------- */

const TitleCard: React.FC<{dur: number; end?: boolean}> = ({dur, end}) => {
	const f = useCurrentFrame();
	const out = end ? 1 : interpolate(f, [dur - 12, dur], [1, 0], clamp);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', fontFamily: SANS, color: C.ink, textAlign: 'center', opacity: out}}>
			<div style={rise(f, 0, 16, 16)}>
				<Symbol size={144} />
			</div>
			<div style={{...rise(f, 8, 16, 16), marginTop: 56, fontSize: 38, fontWeight: 600, color: C.slate, letterSpacing: '0.02em'}}>
				2026 한이음 드림업
			</div>
			<div style={{width: 96 * fadeIn(f, 14, 14), height: 4, background: C.blue, borderRadius: 2, margin: '36px 0 40px'}} />
			<div style={{...rise(f, 16, 18, 20), fontSize: 88, fontWeight: 800, lineHeight: 1.28, letterSpacing: '-0.01em', wordBreak: 'keep-all'}}>
				공공데이터 AI 데이터셋
				<br />
				자동 표준화 및 검증 플랫폼 개발
			</div>
			{end ? (
				<>
					<div style={{...rise(f, 26, 16, 12), marginTop: 44, fontSize: 40, fontWeight: 700}}>
						KPubData <span style={{color: C.slate, fontWeight: 500, fontSize: 34}}>Builder · Studio</span>
					</div>
					<div style={{...rise(f, 32, 16, 8), position: 'absolute', bottom: 54, fontSize: 24, color: C.slate}}>
						화면: 실제 실행 녹화 · AI 도우미 장면은 데모 모드 · 음성·음향 없음
					</div>
				</>
			) : null}
		</AbsoluteFill>
	);
};

/* ---------- 공통: 화면 문구 ---------- */

const Kinetic: React.FC<{text: string; from?: number; top?: number; size?: number}> = ({text, from = 0, top = 120, size = 76}) => {
	const f = useCurrentFrame();
	return (
		<div style={{position: 'absolute', top, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontWeight: 800, fontSize: size, color: C.ink, letterSpacing: '-0.01em', ...rise(f, from, 14, 22)}}>
			{text}
		</div>
	);
};

/* ---------- Q1: 형식은 제각각, 정리는 손으로. ---------- */

const CodeCard: React.FC<{title: string; body: string; at: number; x: number; y: number; rot: number}> = ({title, body, at, x, y, rot}) => {
	const f = useCurrentFrame();
	const t = fadeIn(f, at, 14);
	return (
		<div style={{position: 'absolute', left: x, top: y, width: 470, background: C.bg, border: `2px solid ${C.border}`, borderRadius: 18, padding: '22px 26px', opacity: t, transform: `translateY(${(1 - t) * -40}px) rotate(${rot}deg)`, fontFamily: MONO, fontSize: 22, color: C.ink, lineHeight: 1.55}}>
			<div style={{fontFamily: SANS, fontSize: 22, fontWeight: 700, color: C.slate, marginBottom: 10}}>{title}</div>
			<pre style={{margin: 0, whiteSpace: 'pre-wrap'}}>{body}</pre>
		</div>
	);
};

const Problem1: React.FC = () => {
	const f = useCurrentFrame();
	const rows = [
		['단지', '거래금액', '지역코드', '층'],
		['도곡렉슬', '295,000', '11680', '12'],
		['개포주공6단지', 'N/A', '1168', '3'],
		['대치현대', '186,660', '11680', '-'],
	];
	const bad = new Set(['2-1', '2-2', '3-3', '1-1', '3-1']);
	return (
		<AbsoluteFill style={{background: C.bg}}>
			<Kinetic text="형식은 제각각, 정리는 손으로." top={170} />
			<CodeCard title="기관 A · XML" at={10} x={150} y={420} rot={-2} body={'<item>\n  <aptNm>도곡렉슬</aptNm>\n  <dealAmount>295,000</dealAmount>\n</item>'} />
			<CodeCard title="기관 B · JSON" at={22} x={725} y={450} rot={1.5} body={'{ "APT_NM": "도곡렉슬",\n  "DEAL_AMT": "295000",\n  "YMD": "2024-09" }'} />
			<div style={{position: 'absolute', left: 1300, top: 400, width: 480, opacity: fadeIn(f, 34, 14), fontFamily: SANS}}>
				<div style={{fontSize: 22, fontWeight: 700, color: C.slate, marginBottom: 10}}>내려받은 표</div>
				<div style={{border: `2px solid ${C.border}`, borderRadius: 18, overflow: 'hidden'}}>
					{rows.map((r, i) => (
						<div key={i} style={{display: 'flex', background: i === 0 ? C.muted : C.bg, borderTop: i ? `1px solid ${C.border}` : 'none'}}>
							{r.map((c, j) => {
								const isBad = bad.has(`${i}-${j}`);
								const on = isBad && f > 60 + (i * 4 + j) * 6;
								return (
									<div key={j} style={{flex: j === 0 ? 1.6 : 1, padding: '14px 12px', fontSize: 22, fontWeight: i === 0 ? 700 : 500, color: on ? C.failure : C.ink, background: on ? '#FDECEC' : 'transparent', fontFamily: i === 0 ? SANS : MONO, transition: 'none'}}>
										{c}
									</div>
								);
							})}
						</div>
					))}
				</div>
				<div style={{marginTop: 18, fontSize: 24, color: C.failure, fontWeight: 600, opacity: fadeIn(f, 120, 12)}}>
					결측 표기 · 숫자 속 쉼표 · 앞자리 0 누락
				</div>
			</div>
		</AbsoluteFill>
	);
};

/* ---------- Q2: 기록이 없다. ---------- */

const Problem2: React.FC = () => {
	const f = useCurrentFrame();
	const files = ['clean_v2.py', 'final_final.ipynb', 'fix_amount.py', 'merge(1).csv'];
	return (
		<AbsoluteFill style={{background: C.bg, fontFamily: SANS}}>
			<Kinetic text="기록이 없다." top={200} />
			<div style={{position: 'absolute', top: 440, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 40}}>
				{files.map((name, i) => {
					const t = fadeIn(f, 6 + i * 5, 10);
					const fade = interpolate(f, [60, 100], [1, 0.45], clamp);
					return (
						<div key={name} style={{width: 260, height: 190, border: `2px solid ${C.border}`, borderRadius: 18, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 18, opacity: t * fade, transform: `translateY(${(1 - t) * 30 + i * 8 * Math.sin(i)}px)`}}>
							<div style={{width: 56, height: 70, border: `3px solid ${C.slate}`, borderRadius: 8}} />
							<div style={{fontFamily: MONO, fontSize: 22, color: C.slate}}>{name}</div>
						</div>
					);
				})}
			</div>
			<div style={{position: 'absolute', top: 700, left: 0, right: 0, textAlign: 'center', fontSize: 44, fontWeight: 700, color: C.ink, ...rise(f, 50, 14, 16)}}>
				“어떤 규칙으로 만들었지?”
			</div>
		</AbsoluteFill>
	);
};

/* ---------- B1: KPubData Builder · Studio ---------- */

const Brand: React.FC = () => {
	const f = useCurrentFrame();
	const card = (name: string, role: string, desc: string, at: number) => (
		<div style={{width: 560, border: `2px solid ${C.border}`, borderRadius: 22, padding: '34px 40px', textAlign: 'left', ...rise(f, at, 14, 20)}}>
			<div style={{fontSize: 30, fontWeight: 600, color: C.slate}}>KPubData</div>
			<div style={{fontSize: 64, fontWeight: 800, color: C.ink, marginTop: 4}}>{name}</div>
			<div style={{fontSize: 34, fontWeight: 700, color: C.blue, marginTop: 16}}>{role}</div>
			<div style={{fontSize: 26, color: C.slate, marginTop: 12, lineHeight: 1.45}}>{desc}</div>
		</div>
	);
	return (
		<AbsoluteFill style={{background: C.bg, fontFamily: SANS, alignItems: 'center'}}>
			<div style={{display: 'flex', alignItems: 'center', gap: 30, marginTop: 150, ...rise(f, 0, 14, 14)}}>
				<Symbol size={110} />
				<div style={{fontSize: 96, fontWeight: 800, color: C.ink}}>KPubData</div>
			</div>
			<div style={{display: 'flex', gap: 60, marginTop: 90}}>
				{card('Builder', '실행 엔진', '명세 검증 · Bronze → Silver → Gold\n스냅샷 · Manifest · 읽기 전용 SQL', 26)}
				{card('Studio', '웹 작업공간', '카탈로그 · 테이블 만들기 · SQL 분석\n품질 · 게시 · AI 도우미', 40)}
			</div>
		</AbsoluteFill>
	);
};

/* ---------- B2: 명세 하나로, 기록까지. ---------- */

const Pipeline: React.FC = () => {
	const f = useCurrentFrame();
	const box = (label: string, sub: string, x: number, at: number, w = 250) => (
		<div style={{position: 'absolute', left: x, top: 470, width: w, height: 150, border: `2px solid ${C.border}`, borderRadius: 20, background: C.bg, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', ...rise(f, at, 12, 16)}}>
			<div style={{fontSize: 38, fontWeight: 800, color: C.ink}}>{label}</div>
			<div style={{fontSize: 22, color: C.slate, marginTop: 8}}>{sub}</div>
		</div>
	);
	const line = (x1: number, x2: number, at: number) => (
		<div style={{position: 'absolute', left: x1, top: 543, height: 4, width: (x2 - x1) * fadeIn(f, at, 10), background: C.cyan, borderRadius: 2}} />
	);
	return (
		<AbsoluteFill style={{background: C.bg, fontFamily: SANS}}>
			<Kinetic text="명세 하나로, 기록까지." top={100} />
			<div style={{position: 'absolute', left: 96, top: 400, width: 330, border: `2px solid ${C.blue}`, borderRadius: 20, padding: '20px 24px', fontFamily: MONO, fontSize: 21, lineHeight: 1.6, color: C.ink, ...rise(f, 8, 12, 16)}}>
				<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.blue, marginBottom: 6}}>BuildSpec</div>
				sources:
				<br />
				&nbsp;- datago.apt_trade
				<br />
				quality: …
				<br />
				pii: {'{'}mode: block{'}'}
				<br />
				exports: …
			</div>
			{line(426, 520, 22)}
			{box('Bronze', '원본 보존', 520, 26, 230)}
			{line(750, 800, 34)}
			{box('Silver', '정규화 · 검사', 800, 38, 260)}
			{line(1060, 1110, 46)}
			{box('Gold', '선택 · 분할', 1110, 50, 230)}
			{line(1340, 1390, 58)}
			{box('스냅샷', '읽기 전용', 1390, 62, 250)}
			<div style={{position: 'absolute', left: 520, top: 700, width: 1120, height: 96, borderRadius: 20, background: C.blueTint, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 22, fontSize: 32, fontWeight: 700, color: C.ink, ...rise(f, 80, 12, 14)}}>
				<span style={{color: C.blue}}>Manifest</span>
				<span style={{fontWeight: 500, color: C.slate, fontSize: 28}}>출처 · 행 수 · 품질 결과 · 입력 지문을 실행마다 기록</span>
			</div>
		</AbsoluteFill>
	);
};

/* ---------- 녹화 화면: 창 모형 + 확대 + 배속 표시 ---------- */

const MOCK = {x: 288, y: 78, w: 1344, bar: 30};
const CONTENT_H = (MOCK.w * 900) / 1440;

const cameraAt = (keys: Key[], f: number) => {
	if (f <= keys[0].at) return keys[0];
	for (let i = 1; i < keys.length; i++) {
		const a = keys[i - 1];
		const b = keys[i];
		if (f <= b.at) {
			const t = ease((f - a.at) / Math.max(1, b.at - a.at));
			return {at: f, z: a.z + (b.z - a.z) * t, x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t};
		}
	}
	return keys[keys.length - 1];
};

type Placed = Segment & {start: number; len: number; hold: number};

const placeSegments = (segments: Segment[], dur: number): Placed[] => {
	let t = 0;
	const out = segments.map((s) => {
		const len = Math.round(((s.to - s.from) / (s.rate ?? 1)) * 30);
		const p = {...s, start: t, len, hold: s.hold ?? 0};
		t += len + p.hold;
		return p;
	});
	const last = out[out.length - 1];
	if (t < dur) last.hold += dur - t;
	return out;
};

const Footage: React.FC<{segments: Segment[]; dur: number}> = ({segments, dur}) => {
	const placed = placeSegments(segments, dur);
	return (
		<>
			{placed.map((s, i) => (
				<React.Fragment key={i}>
					<Sequence from={s.start} durationInFrames={s.len} layout="none">
						<OffthreadVideo
							src={staticFile(`footage/${s.src}`)}
							startFrom={Math.round(s.from * 30)}
							playbackRate={s.rate ?? 1}
							muted
							style={{width: '100%', height: '100%'}}
						/>
					</Sequence>
					{s.hold > 0 ? (
						<Sequence from={s.start + s.len} durationInFrames={s.hold} layout="none">
							<Freeze frame={Math.round(s.to * 30) - 1}>
								<OffthreadVideo src={staticFile(`footage/${s.src}`)} muted style={{width: '100%', height: '100%'}} />
							</Freeze>
						</Sequence>
					) : null}
				</React.Fragment>
			))}
		</>
	);
};

const SpeedBadge: React.FC<{segments: Segment[]; dur: number}> = ({segments, dur}) => {
	const f = useCurrentFrame();
	const cur = placeSegments(segments, dur).find((s) => f >= s.start && f < s.start + s.len);
	const rate = cur?.rate ?? 1;
	if (!cur || rate <= 2) return null;
	return (
		<div style={{position: 'absolute', right: 16, top: MOCK.bar + 14, padding: '6px 14px', borderRadius: 999, background: 'rgba(23,32,51,0.78)', color: '#fff', fontFamily: SANS, fontSize: 22, fontWeight: 700}}>
			×{Number.isInteger(rate) ? rate : rate.toFixed(1)}
		</div>
	);
};

const Proof: React.FC<{shot: Extract<Shot, {kind: 'proof'}>; prevKicker?: string}> = ({shot, prevKicker}) => {
	const f = useCurrentFrame();
	const raw = cameraAt(shot.camera, f);
	const cam = {...raw, z: 1 + (raw.z - 1) * ZOOM_DAMP};
	const W = MOCK.w;
	const H = CONTENT_H;
	const tx = Math.min(0, Math.max(W - W * cam.z, W / 2 - cam.x * W * cam.z));
	const ty = Math.min(0, Math.max(H - H * cam.z, H / 2 - cam.y * H * cam.z));
	const newSection = prevKicker !== shot.kicker;
	const head = newSection ? rise(f, 0, 12, 14) : {opacity: 1};
	return (
		<AbsoluteFill style={{background: C.bg, fontFamily: SANS}}>
			<div style={{position: 'absolute', left: MOCK.x, top: 14, right: MOCK.x, height: 54, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
				<div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
					<div style={{fontSize: 26, fontWeight: 700, color: C.slate, ...head}}>{shot.kicker}</div>
					<div style={{fontSize: 38, fontWeight: 800, color: C.ink, ...rise(f, 0, 12, 10)}}>{shot.heading}</div>
				</div>
				{shot.chip ? (
					<div style={{padding: '6px 16px', borderRadius: 999, fontSize: 20, fontWeight: 700, color: shot.chip.tone === 'demo' ? C.warning : C.slate, background: shot.chip.tone === 'demo' ? '#FEF3E2' : C.muted, border: `1.5px solid ${shot.chip.tone === 'demo' ? '#F5C98B' : C.border}`}}>
						{shot.chip.text}
					</div>
				) : null}
			</div>
			<div style={{position: 'absolute', left: MOCK.x, top: MOCK.y, width: W, height: H + MOCK.bar, borderRadius: 18, overflow: 'hidden', border: `1.5px solid ${C.border}`, boxShadow: '0 10px 32px rgba(23,32,51,0.10)', background: C.bg}}>
				<div style={{height: MOCK.bar, background: C.muted, borderBottom: `1px solid ${C.border}`, display: 'flex', alignItems: 'center', padding: '0 16px', gap: 8}}>
					{[0, 1, 2].map((i) => (
						<div key={i} style={{width: 11, height: 11, borderRadius: 6, background: '#D5D9D2'}} />
					))}
					<div style={{flex: 1, textAlign: 'center', fontSize: 16, color: C.slate, fontWeight: 600, marginRight: 52}}>KPubData Studio</div>
				</div>
				<div style={{position: 'relative', width: W, height: H, overflow: 'hidden'}}>
					<div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${cam.z})`}}>
						<Footage segments={shot.segments} dur={shot.dur} />
					</div>
				</div>
				<SpeedBadge segments={shot.segments} dur={shot.dur} />
			</div>
		</AbsoluteFill>
	);
};

/* ---------- F1: 요약 ---------- */

const Recap: React.FC = () => {
	const f = useCurrentFrame();
	const items = ['사전 검증', '단계별 기록', '읽기 전용 스냅샷', '승인 후 실행'];
	return (
		<AbsoluteFill style={{background: C.bg, fontFamily: SANS, alignItems: 'center', justifyContent: 'center'}}>
			<Symbol size={96} style={{...rise(f, 0, 12, 10), marginBottom: 70}} />
			<div style={{display: 'flex', gap: 28}}>
				{items.map((t, i) => (
					<div key={t} style={{padding: '30px 40px', borderRadius: 22, border: `2px solid ${C.border}`, fontSize: 44, fontWeight: 800, color: C.ink, ...rise(f, 6 + i * 6, 12, 18)}}>
						{t}
					</div>
				))}
			</div>
		</AbsoluteFill>
	);
};

/* ---------- 자막: 설명은 모두 자막으로 한다(음성·음향 없음). ---------- */

const Subtitle: React.FC<{text: string; len: number}> = ({text, len}) => {
	const f = useCurrentFrame();
	const o = Math.min(fadeIn(f, 0, 6), interpolate(f, [len - 6, len], [1, 0], clamp));
	return (
		<div style={{position: 'absolute', top: 960, bottom: 8, left: 0, right: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: o}}>
			<div style={{maxWidth: 1500, padding: '8px 28px', borderRadius: 14, background: 'rgba(23,32,51,0.88)', color: '#fff', fontFamily: SANS, fontSize: 33, fontWeight: 600, lineHeight: 1.38, textAlign: 'center', wordBreak: 'keep-all'}}>
				{text}
			</div>
		</div>
	);
};

const captionOf: Record<string, string> = Object.fromEntries((captions as {shot: string; text: string}[]).map((c) => [c.shot, c.text]));

export const Video: React.FC = () => (
	<AbsoluteFill style={{background: C.bg}}>
		{SHOTS.map((s, i) => {
			const prev = SHOTS[i - 1];
			const prevKicker = prev && prev.kind === 'proof' ? prev.kicker : undefined;
			let body: React.ReactNode;
			switch (s.kind) {
				case 'title':
					body = <TitleCard dur={s.dur} />;
					break;
				case 'end':
					body = <TitleCard dur={s.dur} end />;
					break;
				case 'problem1':
					body = <Problem1 />;
					break;
				case 'problem2':
					body = <Problem2 />;
					break;
				case 'brand':
					body = <Brand />;
					break;
				case 'pipeline':
					body = <Pipeline />;
					break;
				case 'recap':
					body = <Recap />;
					break;
				case 'proof':
					body = <Proof shot={s} prevKicker={prevKicker} />;
					break;
			}
			return (
				<Sequence key={s.id} name={s.id} from={starts[i]} durationInFrames={s.dur}>
					{body}
				</Sequence>
			);
		})}
		{SHOTS.map((s, i) =>
			captionOf[s.id] ? (
				<Sequence key={`${s.id}-caption`} name={`${s.id} caption`} from={starts[i] + CAPTION_IN} durationInFrames={s.dur - CAPTION_IN - CAPTION_OUT}>
					<Subtitle text={captionOf[s.id]} len={s.dur - CAPTION_IN - CAPTION_OUT} />
				</Sequence>
			) : null,
		)}
	</AbsoluteFill>
);
