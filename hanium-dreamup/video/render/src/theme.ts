import {continueRender, delayRender, staticFile} from 'remotion';

/** KPubData Brand v2 (kpubdata-studio docs/brand/VISUAL_IDENTITY.md). 바탕은 흰색. */
export const C = {
	bg: '#FFFFFF',
	ink: '#172033',
	slate: '#64748B',
	border: '#E5E7E2',
	muted: '#F1F3EF',
	blue: '#2563EB',
	cyan: '#06B6D4',
	mint: '#14B8A6',
	success: '#15803D',
	warning: '#B45309',
	failure: '#B91C1C',
	blueTint: '#EAF1FE',
};

export const SANS = '"Pretendard", sans-serif';
export const MONO = '"JetBrains Mono", "DejaVu Sans Mono", monospace';
export const FPS = 30;

const handle = delayRender('Pretendard');
const face = new FontFace('Pretendard', `url(${staticFile('PretendardVariable.woff2')}) format("woff2")`, {weight: '100 900'});
face
	.load()
	.then((f) => {
		document.fonts.add(f);
		continueRender(handle);
	})
	.catch((e) => {
		console.error(e);
		continueRender(handle);
	});

/** fast-out / slow-in */
export const ease = (t: number) => {
	const x = Math.min(1, Math.max(0, t));
	return 1 - Math.pow(1 - x, 3);
};
