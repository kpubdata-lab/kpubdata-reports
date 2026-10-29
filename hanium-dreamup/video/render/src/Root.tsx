import React from 'react';
import {Composition} from 'remotion';
import './theme';
import {FPS} from './theme';
import {TOTAL} from './timeline';
import {Video} from './Video';

export const RemotionRoot: React.FC = () => (
	<Composition id="Main" component={Video} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} />
);
