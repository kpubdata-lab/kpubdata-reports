/**
 * 콘티(video-storyboard.md §3)를 프레임 단위로 옮긴 타임라인. 30 fps, 샷 경계는 2초(60프레임) 마디 위.
 * 녹화 구간 시각(초)은 rec/record.cjs가 남긴 *.marks.json을 보고 정했다.
 */
export type Key = {at: number; z: number; x: number; y: number};
/** 녹화 파일의 [from, to]초를 rate 배속으로 재생한다. hold는 마지막 프레임을 멈춰 두는 프레임 수. */
export type Segment = {src: string; from: number; to: number; rate?: number; hold?: number};

export type Shot =
	| {id: string; dur: number; kind: 'title' | 'problem1' | 'problem2' | 'brand' | 'pipeline' | 'recap' | 'end'}
	| {
			id: string;
			dur: number;
			kind: 'proof';
			kicker: string;
			heading: string;
			chip?: {text: string; tone: 'real' | 'demo'};
			segments: Segment[];
			camera: Key[];
	  };

const REAL = {text: '실제 Builder 연동 · 공공데이터포털 API', tone: 'real' as const};

export const SHOTS: Shot[] = [
	{id: 'T1', dur: 120, kind: 'title'},
	{id: 'Q1', dur: 240, kind: 'problem1'},
	{id: 'Q2', dur: 120, kind: 'problem2'},
	{id: 'B1', dur: 180, kind: 'brand'},
	{id: 'B2', dur: 180, kind: 'pipeline'},
	{
		id: 'D1', dur: 120, kind: 'proof', kicker: '01 · 찾기', heading: '카탈로그에서 찾고, 바로 시작.', chip: REAL,
		segments: [{src: 'rec-01-catalog.mp4', from: 0.6, to: 6.9, rate: 1.6}],
		camera: [
			{at: 0, z: 1, x: 0.5, y: 0.5},
			{at: 14, z: 1.45, x: 0.4, y: 0.32},
			{at: 52, z: 1.45, x: 0.4, y: 0.32},
			{at: 72, z: 1.45, x: 0.68, y: 0.4},
			{at: 92, z: 1.45, x: 0.68, y: 0.4},
			{at: 110, z: 1, x: 0.5, y: 0.5},
		],
	},
	{
		id: 'D2', dur: 240, kind: 'proof', kicker: '02 · 만들기', heading: '구성 → 미리보기·검증 → 만들기', chip: REAL,
		segments: [
			{src: 'rec-02-configure.mp4', from: 0.8, to: 9.2, rate: 2.6},
			{src: 'rec-03-preview-run.mp4', from: 0.6, to: 7.8, rate: 2},
		],
		camera: [
			{at: 0, z: 1.25, x: 0.5, y: 0.3},
			{at: 28, z: 1.25, x: 0.5, y: 0.3},
			{at: 44, z: 1.45, x: 0.74, y: 0.6},
			{at: 92, z: 1.45, x: 0.74, y: 0.62},
			{at: 97, z: 1, x: 0.5, y: 0.5},
			{at: 150, z: 1.25, x: 0.45, y: 0.6},
			{at: 200, z: 1.4, x: 0.84, y: 0.48},
			{at: 240, z: 1.4, x: 0.84, y: 0.48},
		],
	},
	{
		id: 'D3', dur: 120, kind: 'proof', kicker: '02 · 만들기', heading: '실행 전에, 먼저 검증.', chip: REAL,
		segments: [{src: 'rec-03-preview-run.mp4', from: 7.8, to: 13.0, rate: 1.3}],
		camera: [
			{at: 0, z: 1.4, x: 0.84, y: 0.48},
			{at: 14, z: 1.4, x: 0.84, y: 0.48},
			{at: 40, z: 1.3, x: 0.5, y: 0.42},
			{at: 100, z: 1.3, x: 0.5, y: 0.42},
			{at: 120, z: 1.1, x: 0.5, y: 0.5},
		],
	},
	{
		id: 'R1', dur: 240, kind: 'proof', kicker: '03 · 실행', heading: '원본은 그대로, 정제는 규칙대로.', chip: REAL,
		segments: [{src: 'rec-03-preview-run.mp4', from: 12.6, to: 18.3, rate: 1, hold: 69}],
		camera: [
			{at: 0, z: 1, x: 0.5, y: 0.5},
			{at: 50, z: 1, x: 0.5, y: 0.5},
			{at: 90, z: 1.55, x: 0.43, y: 0.56},
			{at: 240, z: 1.6, x: 0.43, y: 0.56},
		],
	},
	{
		id: 'R2', dur: 120, kind: 'proof', kicker: '03 · 실행', heading: '단계마다, 결과가 남는다.', chip: REAL,
		segments: [{src: 'rec-03-preview-run.mp4', from: 17.4, to: 20.6, rate: 1, hold: 24}],
		camera: [
			{at: 0, z: 1.6, x: 0.43, y: 0.56},
			{at: 30, z: 1.6, x: 0.4, y: 0.72},
			{at: 120, z: 1.65, x: 0.4, y: 0.72},
		],
	},
	{
		id: 'A1', dur: 120, kind: 'proof', kicker: '04 · 분석', heading: '읽기 전용 스냅샷', chip: REAL,
		segments: [{src: 'rec-04-table.mp4', from: 0.6, to: 5.8, rate: 1.3}],
		camera: [
			{at: 0, z: 1.1, x: 0.5, y: 0.4},
			{at: 40, z: 1.4, x: 0.45, y: 0.3},
			{at: 120, z: 1.45, x: 0.45, y: 0.3},
		],
	},
	{
		id: 'A2', dur: 240, kind: 'proof', kicker: '04 · 분석', heading: '같은 스냅샷, 같은 결과.', chip: REAL,
		segments: [
			{src: 'rec-05-sql.mp4', from: 0.6, to: 2.6, rate: 1.25},
			{src: 'rec-05-sql.mp4', from: 2.7, to: 10.2, rate: 5},
			{src: 'rec-05-sql.mp4', from: 10.2, to: 13.8, rate: 2},
			{src: 'rec-05-sql.mp4', from: 13.8, to: 22.4, rate: 2.8},
		],
		camera: [
			{at: 0, z: 1.3, x: 0.35, y: 0.25},
			{at: 45, z: 1.4, x: 0.55, y: 0.28},
			{at: 100, z: 1.4, x: 0.6, y: 0.35},
			{at: 130, z: 1.05, x: 0.55, y: 0.55},
			{at: 240, z: 1.1, x: 0.6, y: 0.6},
		],
	},
	{
		id: 'G1', dur: 180, kind: 'proof', kicker: '05 · AI 도우미', heading: 'AI는 제안, 실행은 사용자.',
		chip: {text: '데모 모드 · mock 데이터', tone: 'demo'},
		segments: [
			{src: 'rec-07-assistant.mp4', from: 0.6, to: 8.4, rate: 2.6},
			{src: 'rec-07-assistant.mp4', from: 8.4, to: 15.1, rate: 2.2},
		],
		camera: [
			{at: 0, z: 1, x: 0.5, y: 0.5},
			{at: 20, z: 1.3, x: 0.8, y: 0.5},
			{at: 88, z: 1.3, x: 0.8, y: 0.55},
			{at: 110, z: 1.55, x: 0.8, y: 0.6},
			{at: 180, z: 1.6, x: 0.8, y: 0.68},
		],
	},
	{
		id: 'G2', dur: 180, kind: 'proof', kicker: '06 · 게시', heading: '게시 전에, Builder가 점검.', chip: REAL,
		segments: [{src: 'rec-06-publish.mp4', from: 0.6, to: 7.4, rate: 1.13}],
		camera: [
			{at: 0, z: 1.3, x: 0.42, y: 0.5},
			{at: 60, z: 1.3, x: 0.42, y: 0.55},
			{at: 180, z: 1.25, x: 0.5, y: 0.6},
		],
	},
	{id: 'F1', dur: 120, kind: 'recap'},
	{id: 'F2', dur: 120, kind: 'end'},
];

export const starts = (() => {
	let t = 0;
	return SHOTS.map((s) => {
		const at = t;
		t += s.dur;
		return at;
	});
})();

export const TOTAL = SHOTS.reduce((a, s) => a + s.dur, 0);

/** 샷 시작 후 내레이션이 들어가는 프레임. */
export const NARRATION_OFFSET = 8;
