import {Config} from '@remotion/cli/config';

// 영상 합성용 크롬. 설치된 Google Chrome을 쓰면 Remotion이 따로 내려받지 않는다.
Config.setBrowserExecutable(process.env.REMOTION_CHROME ?? null);
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(16);
Config.setPixelFormat('yuv420p');
