---
name: history-animation-video
description: Create customized historical-figure AI animation video self-media plans, viral short-video hooks, workflows, scripts, storyboards, image/video prompts, low-cost tool stacks, overseas publishing plans, content calendars, and API-ready one-click production systems. Use when the user asks to enter history character animation video, make viral AI historical shorts, customize a creator account, generate a one-click media plan, produce scripts/storyboards/prompts for historical figures, compare cost-effective AI video production workflows, or publish historical animation content on foreign platforms.
---

# History Animation Video

## Overview

Produce a concrete, creator-ready plan for historical-figure AI animation video accounts. Default to Chinese output unless the user requests another language.

## Quick Start

For a one-click offline baseline, run:

```bash
python3 ~/.codex/skills/history-animation-video/scripts/customize_channel.py \
  --platform douyin \
  --budget low \
  --niche "中国历史人物高光转折" \
  --style cinematic \
  --output ~/Desktop/history-animation-plan.md
```

For a one-click production package with API-ready jobs, run:

```bash
python3 ~/.codex/skills/history-animation-video/scripts/one_click_pipeline.py \
  --project "秦始皇第一条样片" \
  --platform douyin \
  --figure "秦始皇" \
  --topic "统一之后，他最害怕的不是六国余孽" \
  --style cinematic \
  --output-dir ~/Desktop/history-video-project
```

If the user asks Codex to customize directly, collect missing inputs only when needed. If the user says "一键", "直接生成", or "别问了", use sensible defaults and proceed.

## Inputs

Use or infer these fields:

- Platform: Douyin, Bilibili, Xiaohongshu, YouTube Shorts, TikTok, Instagram Reels, Facebook Reels, Snapchat Spotlight, Pinterest, X, or mixed.
- Audience: students, office workers, parents, history fans, overseas Chinese, or general public.
- Niche: Chinese history, world history, emperors, generals, women in history, strategists, scientists, local history, mythology-adjacent history.
- Style: cinematic, ink-painting, anime, documentary, comic, clay, paper-cut.
- Budget: free, low, pro, team.
- Capacity: videos per week, video duration, editing skill, voice preference.
- Constraint: no face, no paid tool, phone-only, overseas platform, monetization target, etc.

Ask at most three short clarifying questions. Do not block on perfect answers.

## Output Contract

Return a complete plan with these sections:

1. Account positioning: account name direction, audience, promise, differentiation, and avoid list.
2. Content pillars: 3-5 repeatable series formats with title formulas.
3. Cost-effective tool stack: writing/research, image, video, voice, music, editing, subtitles, publishing analytics. If current pricing or availability matters, browse/verify official sources before final recommendations.
4. Production SOP: research -> script -> storyboard -> character sheet -> image prompts -> video prompts -> voice -> edit -> publish -> review.
5. Reusable prompt pack: script prompt, fact-check prompt, character prompt, scene prompt, motion prompt, voice direction, title/cover prompt.
6. First 10 videos: title, hook, historical figure, conflict, visual idea, expected duration.
7. First video package: full short script, shot list, image prompts, video prompts, narration, cover/title variants.
8. 30-day execution calendar: daily work, weekly publishing cadence, review metrics.
9. Compliance and risk: AI label, historical uncertainty, copyright, platform sensitivity, ad/monetization constraints.
10. Iteration rules: what metrics to track and how to adjust next batch.
11. Viral distribution pack: hook variants, title/cover A/B tests, retention beats, comment triggers, remix/reply prompts, and cross-platform rewrite rules.
12. Overseas platform matrix: primary platforms, secondary platforms, language strategy, recommended cadence, and format changes.
13. If APIs are provided: produce a safe `.env` plan, provider config, adapter mapping, and one-click command. Never hard-code API keys in generated code or markdown.

Keep outputs concrete. Avoid generic advice unless it directly informs a decision.

## Workflow

1. Choose a narrow market:
   - Start with one dynasty/region/theme instead of "all history".
   - Prefer repeatable conflicts: betrayal, reform, exile, comeback, final decision, unlikely alliance.
2. Build one reusable format:
   - 35-75 seconds for viral short platforms, 90-180 seconds only when the platform rewards deeper context.
   - Hook in first 3 seconds.
   - 6-10 shots.
   - One historical question, one turning point, one emotional payoff.
3. Engineer shareability:
   - Start with an open loop: contradiction, taboo choice, ignored cost, or "history remembers the wrong thing".
   - Add pattern interrupts every 2-4 seconds: object close-up, map shift, sudden silence, quote card, crowd reaction.
   - End with a debate prompt that has two defensible sides; do not end with generic "follow for more".
4. Preserve character consistency:
   - Create a character sheet before scene prompts.
   - Reuse clothing, age, facial traits, palette, and camera language.
5. Separate factual and dramatic layers:
   - Mark known facts, plausible inference, and dramatized dialogue.
   - Avoid presenting uncertain legends as verified facts.
6. Optimize for batch production:
   - Generate 10 scripts first.
   - Produce visual prompts from a shared template.
   - Edit with the same subtitle, music, and cover system.

## References

- Read `references/content-system.md` when building positioning, topic systems, scripts, or calendars.
- Read `references/viral-growth.md` when optimizing for fast spread, retention, comments, titles, covers, and A/B testing.
- Read `references/global-platforms.md` when recommending foreign publishing platforms or adapting one video for multiple overseas channels.
- Read `references/prompt-templates.md` when producing character, image, video, voice, cover, and title prompts.
- Read `references/tool-stack.md` when comparing low-cost production stacks. Verify current prices from official sources before recommending paid subscriptions.
- Read `references/api-integration.md` when connecting user-provided APIs into the one-click pipeline.
