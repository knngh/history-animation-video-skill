# History Animation Video Skill

Codex skill for creating viral historical-figure AI animation video workflows.

It helps generate:

- creator account positioning
- viral topic systems
- scripts and storyboards
- character, image, video, voice, cover, and title prompts
- domestic and overseas distribution plans
- API-ready one-click production job specs
- A/B test packs and review metrics

## Install

Copy this folder into your Codex skills directory:

```bash
cp -R history-animation-video-skill ~/.codex/skills/history-animation-video
```

Then invoke it in Codex with:

```text
Use $history-animation-video to customize my historical AI animation video account.
```

## Quick Start

Generate a channel plan:

```bash
python3 scripts/customize_channel.py \
  --platform douyin \
  --budget low \
  --niche "中国历史人物高光转折" \
  --style cinematic \
  --output ./out/channel-plan.md
```

Generate one API-ready project package:

```bash
python3 scripts/one_click_pipeline.py \
  --project "秦始皇第一条样片" \
  --platform douyin \
  --figure "秦始皇" \
  --topic "统一之后，他最害怕的不是六国余孽" \
  --style cinematic \
  --output-dir ./out
```

## Supported Platforms

Domestic:

- Douyin
- Kuaishou
- WeChat Channels
- Xiaohongshu
- Bilibili
- Xigua
- Zhihu
- Weibo
- Baijiahao

Overseas:

- YouTube Shorts
- TikTok
- Instagram Reels
- Facebook Reels
- Snapchat Spotlight
- Pinterest
- X

## API Integration

The pipeline is designed to connect user-provided APIs for text, image, video, voice, editing, and publishing.

Do not commit API keys. Put secrets in `.env` and use:

- `references/api-setup-cost-effective.md`
- `references/api-config.siliconflow.example.json`
- `references/env.siliconflow.example`
- `references/api-config.example.json`
- `references/env.example`
- `references/api-integration.md`

## Main Files

- `SKILL.md`: Codex skill instructions
- `scripts/customize_channel.py`: channel plan generator
- `scripts/one_click_pipeline.py`: one-video production package generator
- `references/viral-growth.md`: viral structure and A/B testing
- `references/domestic-platforms.md`: Chinese platform distribution strategy
- `references/global-platforms.md`: overseas distribution strategy
- `references/api-setup-cost-effective.md`: low-cost API configuration plan
- `references/prompt-templates.md`: reusable prompts
- `references/tool-stack.md`: cost-effective tool choices
