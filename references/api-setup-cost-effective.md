# Cost-Effective API Setup

Use this guide when configuring APIs for the historical AI animation video pipeline.

## Recommended MVP Stack

Start with one provider:

- Provider: SiliconFlow
- Why: one API account can cover text, image, voice, and video stages.
- Best for: low-cost validation, Chinese content, fast iteration, fewer adapters.

Then upgrade only the bottleneck:

- Text bottleneck: add DeepSeek direct API.
- English voice bottleneck: add ElevenLabs.
- Premium video bottleneck: add Kling, Hailuo/MiniMax, Runway, Luma, or another provider after sample testing.
- Publishing bottleneck: keep manual publishing first; add upload APIs only after the format has stable metrics.

## What You Need To Provide

Minimum:

```text
SILICONFLOW_API_KEY
```

Optional:

```text
DEEPSEEK_API_KEY
ELEVENLABS_API_KEY
VIDEO_API_KEY
YOUTUBE_CLIENT_ID
YOUTUBE_CLIENT_SECRET
```

Do not paste real keys into Markdown files or GitHub. Store them in `.env`.

## Current Pipeline Support

Already implemented:

- `openai_compatible_chat`: live text generation through `/chat/completions`.

API-ready but adapter pending:

- `siliconflow_image`: generate shot images and download them locally.
- `siliconflow_tts`: generate narration audio and save it locally.
- `siliconflow_video`: submit video jobs, poll status, download videos locally.
- `edit`: local FFmpeg/CapCut/Jianying workflow.
- `upload`: manual review first; platform upload APIs later.

## Example Files

Use:

- `references/api-config.siliconflow.example.json`
- `references/env.siliconflow.example`

Run:

```bash
python3 scripts/one_click_pipeline.py \
  --project "秦始皇第一条样片" \
  --platform douyin \
  --figure "秦始皇" \
  --topic "统一之后，他最害怕的不是六国余孽" \
  --style cinematic \
  --config ./providers.json \
  --env-file ./.env \
  --live \
  --output-dir ./out
```

## Cost Control Rules

- Generate scripts first; do not spend video credits until the hook is strong.
- Generate 1 character reference image before 7 shot images.
- Generate low-cost images first, then only upscale the winning shots.
- Generate 1 video clip as a motion test before producing all shots.
- Keep publishing manual until a format has reliable retention and follow conversion.
