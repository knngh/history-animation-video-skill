# API Integration

Use this reference when the user provides APIs and wants one-click production.

## Rule

Never ask the user to paste secret keys into generated Markdown or source files. Store keys in a local `.env` file or existing secret manager, and reference them through environment variable names.

## Minimum Information To Request

Ask for only what is needed:

- Tool name and stage: text, image, video, voice, edit, upload, analytics.
- API documentation URL or request/response examples.
- Authentication method and the environment variable name to use.
- Output format: image URL/file, video URL/file, audio URL/file, job ID polling, webhook.
- Rate limits, cost constraints, and commercial-use constraints if known.

Do not require the user to choose all tools upfront. Build around the stages they can provide first.

## Adapter Contract

Every provider adapter should behave like this:

```text
input: validated job spec from 04_api_jobs.json
output: local artifact path plus metadata JSON
errors: structured message with provider, stage, retryable, and raw status code if available
```

Stages:

- text: generate or improve script.
- image: generate character sheet and shot stills.
- video: turn stills or prompts into clips.
- voice: synthesize narration audio.
- edit: combine clips, audio, subtitles, music, and cover.
- upload: publish only after explicit user confirmation unless the user has already asked for auto-publish.

## Config Shape

Use JSON for provider config and `.env` for secrets:

```json
{
  "providers": {
    "text": {
      "type": "openai_compatible_chat",
      "baseUrl": "https://example.com/v1",
      "model": "replace-with-model",
      "apiKeyEnv": "TEXT_API_KEY",
      "temperature": 0.7,
      "timeout": 90
    },
    "image": {
      "type": "provider_specific",
      "name": "replace-with-image-tool",
      "apiKeyEnv": "IMAGE_API_KEY"
    },
    "video": {
      "type": "provider_specific",
      "name": "replace-with-video-tool",
      "apiKeyEnv": "VIDEO_API_KEY"
    },
    "voice": {
      "type": "provider_specific",
      "name": "replace-with-voice-tool",
      "apiKeyEnv": "VOICE_API_KEY"
    }
  }
}
```

Example `.env`:

```bash
TEXT_API_KEY=replace_me
IMAGE_API_KEY=replace_me
VIDEO_API_KEY=replace_me
VOICE_API_KEY=replace_me
```

## One-Click Command

After config exists:

```bash
python3 ~/.codex/skills/history-animation-video/scripts/one_click_pipeline.py \
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

## Implementation Order

Connect APIs in this order:

1. Text adapter: easiest to validate and cheapest to retry.
2. Image adapter: lock character consistency before video spend.
3. Voice adapter: deterministic and easy to inspect.
4. Video adapter: expensive and slower, run after prompts are stable.
5. Edit/export adapter: only automate after file naming is stable.
6. Upload adapter: keep manual confirmation by default.

## Safety Checks

- Validate every third-party response before using URLs, file paths, or generated text.
- Download generated media to local project folders instead of relying on temporary URLs.
- Save provider response metadata next to artifacts for debugging and cost review.
- Add retry only for retryable status codes or explicit pending jobs.
- Do not auto-publish without a final review gate unless explicitly requested.
