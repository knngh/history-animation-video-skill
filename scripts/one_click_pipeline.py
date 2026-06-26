#!/usr/bin/env python3
"""Create an API-ready project package for one historical AI animation video.

The script intentionally works without third-party packages. In scaffold mode it
generates all files needed for production. In live mode it can call a configured
OpenAI-compatible text endpoint; image/video/voice providers are left as explicit
job specs until provider-specific adapters are added from user API docs.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any


PLATFORM_DEFAULTS = {
    "douyin": {"name": "抖音", "ratio": "9:16", "duration": "60 秒"},
    "xiaohongshu": {"name": "小红书", "ratio": "3:4 或 9:16", "duration": "45-75 秒"},
    "bilibili": {"name": "B站", "ratio": "16:9 或 9:16", "duration": "90-180 秒"},
    "youtube": {"name": "YouTube Shorts", "ratio": "9:16", "duration": "45-60 秒"},
    "tiktok": {"name": "TikTok", "ratio": "9:16", "duration": "35-60 秒"},
    "instagram": {"name": "Instagram Reels", "ratio": "9:16", "duration": "30-60 秒"},
    "facebook": {"name": "Facebook Reels", "ratio": "9:16", "duration": "45-90 秒"},
    "snapchat": {"name": "Snapchat Spotlight", "ratio": "9:16", "duration": "15-45 秒"},
    "pinterest": {"name": "Pinterest", "ratio": "9:16 或 2:3", "duration": "15-60 秒"},
    "x": {"name": "X", "ratio": "9:16 或 16:9", "duration": "30-90 秒"},
}

STYLE_PROMPTS = {
    "cinematic": "cinematic historical animation, realistic lighting, low saturation, dramatic close-up",
    "ink": "Chinese ink wash animation, rice paper texture, elegant negative space, slow poetic framing",
    "anime": "historical anime style, clean line art, expressive face, dynamic composition",
    "documentary": "animated documentary style, archival texture, restrained color, historical illustration",
    "comic": "historical comic panel style, bold contrast, expressive composition, clean outlines",
    "paper-cut": "paper-cut shadow puppet animation, layered paper texture, folk color palette",
}

ENGLISH_FIGURE_NAMES = {
    "凯撒": "Julius Caesar",
    "克娄巴特拉": "Cleopatra",
    "拿破仑": "Napoleon",
    "贞德": "Joan of Arc",
    "林肯": "Abraham Lincoln",
    "伊丽莎白一世": "Elizabeth I",
    "丘吉尔": "Winston Churchill",
    "甘地": "Gandhi",
    "特斯拉": "Nikola Tesla",
    "曼德拉": "Nelson Mandela",
    "秦始皇": "Qin Shi Huang",
    "霍去病": "Huo Qubing",
    "诸葛亮": "Zhuge Liang",
    "李世民": "Li Shimin",
    "武则天": "Wu Zetian",
    "岳飞": "Yue Fei",
    "张居正": "Zhang Juzheng",
    "苏轼": "Su Shi",
    "王阳明": "Wang Yangming",
    "林则徐": "Lin Zexu",
}


@dataclass(frozen=True)
class ProjectInput:
    project: str
    platform: str
    figure: str
    topic: str
    style: str
    duration: str
    language: str
    output_dir: Path
    config: Path | None
    env_file: Path | None
    live: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a one-click historical animation project package.")
    parser.add_argument("--project", required=True, help="Project/video name.")
    parser.add_argument("--platform", default="douyin", choices=sorted(PLATFORM_DEFAULTS))
    parser.add_argument("--figure", required=True, help="Historical figure.")
    parser.add_argument("--topic", required=True, help="Core conflict or hook.")
    parser.add_argument("--style", default="cinematic", choices=sorted(STYLE_PROMPTS))
    parser.add_argument("--duration", default="", help="Override target duration.")
    parser.add_argument("--language", default="中文")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--config", default="", help="Optional provider config JSON.")
    parser.add_argument("--env-file", default="", help="Optional local .env file.")
    parser.add_argument("--live", action="store_true", help="Call configured live APIs where adapters exist.")
    return parser.parse_args()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value.strip(), flags=re.UNICODE)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned or "history-video"


def load_env(path: Path | None) -> None:
    if not path:
        return
    if not path.exists():
        raise FileNotFoundError(f"env file not found: {path}")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def load_config(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"missing environment variable: {name}")
    return value


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def english_figure_name(figure: str) -> str:
    return ENGLISH_FIGURE_NAMES.get(figure, figure)


def openai_compatible_chat(config: dict[str, Any], prompt: str) -> str:
    base_url = str(config.get("baseUrl", "")).rstrip("/")
    model = config.get("model")
    api_key_env = config.get("apiKeyEnv")
    if not base_url or not model or not api_key_env:
        raise RuntimeError("text provider requires baseUrl, model, and apiKeyEnv")

    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是历史动画短视频编剧和传播编辑，输出必须可直接用于生产，且要兼顾历史可信度和短视频传播性。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": float(config.get("temperature", 0.7)),
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {require_env(str(api_key_env))}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=int(config.get("timeout", 90))) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"text API failed: HTTP {exc.code}: {detail}") from exc

    try:
        return str(body["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"unexpected text API response shape: {body}") from exc


def build_script(project: ProjectInput, config: dict[str, Any]) -> str:
    platform = PLATFORM_DEFAULTS[project.platform]
    prompt = dedent(
        f"""
        请为历史人物 AI 动画短视频写一条可直接制作、适合快速传播的脚本。

        项目：{project.project}
        平台：{platform["name"]}
        画幅：{platform["ratio"]}
        时长：{project.duration}
        人物：{project.figure}
        主题/钩子：{project.topic}
        风格：{STYLE_PROMPTS[project.style]}
        语言：{project.language}

        输出格式：
        1. 标题备选 5 个：好奇型、冲突型、情绪型、反转型、搜索型
        2. 口播脚本，按 0-1 秒、1-3 秒、3-8 秒、8-25 秒、25-45 秒、结尾拆分
        3. 事实核验提示：哪些是史实、哪些是合理推断、哪些是艺术化表达
        4. 评论区引导问题 3 个，必须两边都能争
        5. 封面文案 3 个，均不超过 7 个汉字或 5 个英文词
        """
    ).strip()
    text_provider = config.get("providers", {}).get("text", {})
    if project.live and text_provider.get("type") == "openai_compatible_chat":
        return openai_compatible_chat(text_provider, prompt)

    return dedent(
        f"""
        # {project.project} - 脚本

        ## 标题备选

        1. 好奇型：《{project.figure}真正害怕的不是敌人》
        2. 冲突型：《他赢了，却从这里开始失控》
        3. 情绪型：《这一步之后，他再也回不了头》
        4. 反转型：《历史记住了胜利，却漏掉了代价》
        5. 搜索型：《{project.figure}关键选择：胜利背后的代价》

        ## 口播脚本

        0-1 秒：
        屏幕字幕：他赢了，但更危险的事才刚开始。

        1-3 秒：
        历史记住了{project.figure}的胜利，却很少讲他赢完之后失去了什么。

        3-8 秒：
        那一刻，他面对的不是一个简单敌人，而是一条不能回头的路。

        8-25 秒：
        退一步，之前拥有的一切都可能崩塌；进一步，他要承担所有人的恐惧和反对。最难的不是下令，而是知道这道令会让多少人开始害怕他。

        25-45 秒：
        {project.topic}。这不是一句标题，而是这个人物最值得被重新观看的瞬间。真正改变历史的，不是胜利后的欢呼，而是他按下决定前的几秒钟。

        结尾：
        如果你站在他的位置，这是果断，还是赌徒式冒险？

        ## 事实核验提示

        - 确定史实：人物、时代、主要事件需要用可靠资料核对。
        - 合理推断：人物心理只能写成“可能”“或许”“可以理解为”。
        - 艺术化表达：沉默、烛光、转身、独白属于视觉化叙事，不要包装成史书记载。

        ## 评论区问题

        - 如果你是{project.figure}，会做同样选择吗？
        - 这是果断，还是赌徒式冒险？
        - 你认为他最大的代价，是失去敌人，还是失去信任？

        ## 封面文案

        - 没有退路
        - 赢后的代价
        - 他敢吗
        """
    ).strip()


def storyboard_rows(project: ProjectInput) -> list[dict[str, str]]:
    return [
        {
            "shot": "1",
            "time": "0-1s",
            "visual": "人物背影骤停，红色短字幕：他赢了，但更危险的事才刚开始",
            "motion": "快速推近后瞬间停顿，低鼓点",
            "voice": "他赢了，但更危险的事才刚开始。",
        },
        {
            "shot": "2",
            "time": "1-3s",
            "visual": "人物烛光近景，眼神压住情绪",
            "motion": "镜头轻微推近，烛火微动",
            "voice": f"历史记住了{project.figure}的胜利，却很少讲他赢完之后失去了什么。",
        },
        {
            "shot": "3",
            "time": "3-8s",
            "visual": "地图、诏书、剑柄或战报特写",
            "motion": "手指按住关键物件，字幕盖章：没有退路",
            "voice": "那一刻，他面对的不是一个简单敌人，而是一条不能回头的路。",
        },
        {
            "shot": "4",
            "time": "8-20s",
            "visual": "朝堂、军帐或宫门外的群像压力",
            "motion": "远景横移，人群静默",
            "voice": "退一步，之前拥有的一切都可能崩塌。",
        },
        {
            "shot": "5",
            "time": "20-35s",
            "visual": "人物做出决定，转身或抬眼",
            "motion": "从低头到抬眼，镜头停顿",
            "voice": "进一步，他要承担所有人的恐惧和反对。",
        },
        {
            "shot": "6",
            "time": "35-52s",
            "visual": "大门打开、旗帜扬起、尘土或雨幕",
            "motion": "慢动作大场面，光线变化",
            "voice": f"{project.topic}。",
        },
        {
            "shot": "7",
            "time": "52-60s",
            "visual": "人物近景定格，封面式字幕问题",
            "motion": "轻微推近后定格",
            "voice": "如果你站在他的位置，这是果断，还是赌徒式冒险？",
        },
    ]


def build_character_sheet(project: ProjectInput) -> str:
    return dedent(
        f"""
        # 角色设定表

        - 人物：{project.figure}
        - 风格：{STYLE_PROMPTS[project.style]}
        - 年龄段：按该人物关键事件时期设定，避免过度年轻化。
        - 体型：符合历史身份，不做奇幻夸张。
        - 脸型和五官：清晰、稳定、可复用，避免每个镜头换脸。
        - 服装：符合时代身份，颜色控制在 2-3 个主色。
        - 标志物：地图、诏书、印玺、剑、竹简、烛火等，按主题选择。
        - 表情范围：克制、紧张、沉思、决断。
        - 禁止元素：现代建筑、现代服装、影视剧同款造型、文字水印、过度玄幻盔甲。
        """
    ).strip()


def build_prompts(project: ProjectInput, rows: list[dict[str, str]]) -> str:
    style = STYLE_PROMPTS[project.style]
    blocks = [
        "# 图像和视频提示词",
        "",
        "## 角色定妆图",
        "",
        (
            f"{project.figure}, historical character design sheet, {style}, "
            "front view and three-quarter view, consistent face, detailed costume, "
            "neutral background, no text, no watermark, no modern objects"
        ),
        "",
    ]
    for row in rows:
        blocks.extend(
            [
                f"## 镜头 {row['shot']} 图像提示词",
                "",
                (
                    f"{project.figure}, {row['visual']}, {style}, historical animation still, "
                    "consistent character, high detail, cinematic composition, no text, no watermark, no modern objects"
                ),
                "",
                f"## 镜头 {row['shot']} 视频提示词",
                "",
                (
                    f"Use the reference image as the first frame. Generate a 4-6 second shot: {row['motion']}. "
                    "Keep the face, clothing, age, and scene consistent. Do not add new characters. No text."
                ),
                "",
            ]
        )
    return "\n".join(blocks).strip()


def build_api_jobs(project: ProjectInput, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "schemaVersion": "1.0",
        "project": project.project,
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "providers": {
            "text": {"status": "script generated"},
            "image": {"status": "adapter pending", "expectedOutput": "assets/images/shot-XX.png"},
            "video": {"status": "adapter pending", "expectedOutput": "assets/videos/shot-XX.mp4"},
            "voice": {"status": "adapter pending", "expectedOutput": "assets/audio/narration.wav"},
            "edit": {"status": "manual or adapter pending", "expectedOutput": "exports/final.mp4"},
            "publish": {"status": "manual review recommended"},
        },
        "jobs": [
            {
                "id": f"image-shot-{row['shot']}",
                "type": "image",
                "shot": row["shot"],
                "inputFrom": f"03_prompts.md#镜头-{row['shot']}-图像提示词",
                "output": f"assets/images/shot-{int(row['shot']):02d}.png",
            }
            for row in rows
        ]
        + [
            {
                "id": f"video-shot-{row['shot']}",
                "type": "video",
                "shot": row["shot"],
                "inputFrom": f"assets/images/shot-{int(row['shot']):02d}.png",
                "output": f"assets/videos/shot-{int(row['shot']):02d}.mp4",
            }
            for row in rows
        ]
        + [
            {
                "id": "voice-narration",
                "type": "voice",
                "inputFrom": "01_script.md",
                "output": "assets/audio/narration.wav",
            },
            {
                "id": "edit-final",
                "type": "edit",
                "inputFrom": ["assets/videos/*.mp4", "assets/audio/narration.wav", "02_storyboard.csv"],
                "output": "exports/final.mp4",
            },
        ],
    }


def write_storyboard(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["shot", "time", "visual", "motion", "voice"])
        writer.writeheader()
        writer.writerows(rows)


def build_publish_pack(project: ProjectInput) -> str:
    return dedent(
        f"""
        # 发布包

        ## 标题

        - 好奇型：{project.figure}真正害怕的不是敌人
        - 冲突型：他赢了，却从这里开始失控
        - 情绪型：这一步之后，他再也回不了头
        - 反转型：历史记住了胜利，却漏掉了代价
        - 搜索型：{project.figure}关键选择：胜利背后的代价

        ## 封面文案

        - 他没有退路
        - 赢后的代价
        - 这是果断吗

        ## 简介

        用 AI 动画重看{project.figure}的关键一刻：{project.topic}。视频含艺术化演绎，历史信息请以可靠史料为准。

        ## 标签

        #历史人物 #AI动画 #历史故事 #{project.figure} #短视频

        ## 评论种子

        这是果断，还是赌徒式冒险？我更倾向于前者，但代价确实太大。

        ## 发布前检查

        - 已确认无未授权影视截图、音乐、字体或他人作品。
        - 已标注 AI 生成或 AI 辅助。
        - 已检查人物、时代、服饰和关键事件没有明显错误。
        - 已导出无水印版本。
        """
    ).strip()


def build_editing_plan(project: ProjectInput) -> str:
    return dedent(
        f"""
        # 剪辑方案

        - 画幅：{PLATFORM_DEFAULTS[project.platform]["ratio"]}
        - 时长：{project.duration}
        - 字幕：大字号、强对比、每行不超过 14 个汉字。
        - 开头：第 0 秒必须出现冲突字幕或强画面，不要 logo 和片头。
        - 节奏：每 2-4 秒有画面变化，关键句前留 0.2-0.4 秒停顿。
        - 中段：第 8-20 秒必须出现一个具体物件，避免纯旁白。
        - 音乐：低频鼓点或紧张氛围，不压过旁白。
        - 转场：少用花哨转场，优先硬切、淡入、轻微推拉。
        - 片尾：保留 1 秒评论问题，不要做长片尾。
        - A/B 测试：同一视频至少导出 2 个封面、2 个标题、2 个第一句。
        """
    ).strip()


def build_viral_distribution_pack(project: ProjectInput) -> str:
    english_name = english_figure_name(project.figure)
    return dedent(
        f"""
        # 传播和海外分发包

        ## 传播钩子

        - 视觉钩子：人物背影 + 危险字幕“他赢了，但更危险的事才刚开始”
        - 反常识钩子：历史记住了{project.figure}的胜利，却很少讲他赢完之后失去了什么。
        - 选择钩子：如果你是{project.figure}，这一局你敢不敢押？

        ## A/B 测试

        标题：
        - A：{project.figure}真正害怕的不是敌人
        - B：他赢了，却从这里开始失控
        - C：历史记住了胜利，却漏掉了代价

        封面：
        - A：没有退路
        - B：赢后的代价
        - C：他敢吗

        第一句：
        - A：他赢了，但更危险的事才刚开始。
        - B：历史记住了他的胜利，却忘了他的代价。
        - C：如果你是他，这一步你敢不敢走？

        结尾：
        - 评论版：这是果断，还是赌徒式冒险？
        - 系列版：下一集讲他赢完之后，真正失去的东西。

        ## 国外平台分发

        - YouTube Shorts：标题偏搜索，描述写清人物和事件，建“History's Turning Points”播放列表。
        - TikTok：开头更狠，减少背景，评论区置顶“Would you make the same choice?”
        - Instagram Reels：封面统一，Caption 写成短诗感或电影感，适合主页沉淀。
        - Facebook Reels：旁白更直白，减少悬浮表达，适合可分享的道德选择。
        - Snapchat Spotlight：剪成 15-35 秒超短版，只保留对象钩子和选择。
        - Pinterest：输出竖版封面、时间线图和视频 Pin，做常青搜索。
        - X：视频配 4-6 条 thread：观点、史实、推断、争议问题、制作说明。

        ## 英文改写

        - Title A: History remembers his victory. It forgot the price.
        - Title B: The moment {english_name} had no way back.
        - Hook: He won. But what came after victory was more dangerous.
        - Caption: An AI-assisted historical animation about one irreversible choice. Some scenes are dramatized; historical claims should be checked against reliable sources.

        ## 复盘指标

        - 1 秒停留：看封面和第一帧。
        - 3 秒留存：看钩子是否成立。
        - 完播率：看节奏和时长。
        - 评论/千次播放：看结尾问题。
        - 收藏：看知识增量。
        - 分享：看反常识和情绪强度。
        - 关注转化：看栏目是否稳定。
        """
    ).strip()


def write_readme(project: ProjectInput, path: Path) -> None:
    command = (
        "python3 ~/.codex/skills/history-animation-video/scripts/one_click_pipeline.py "
        f"--project {json.dumps(project.project, ensure_ascii=False)} "
        f"--platform {project.platform} "
        f"--figure {json.dumps(project.figure, ensure_ascii=False)} "
        f"--topic {json.dumps(project.topic, ensure_ascii=False)} "
        f"--style {project.style} "
        f"--output-dir {json.dumps(str(project.output_dir.parent), ensure_ascii=False)}"
    )
    write_text(
        path,
        dedent(
            f"""
            # {project.project}

            这个目录是历史人物 AI 动画短视频的一键项目包。

            ## 文件

            - `00_manifest.json`：项目元数据。
            - `01_script.md`：口播脚本和事实核验提示。
            - `02_storyboard.csv`：分镜表。
            - `03_prompts.md`：角色、图像、视频提示词。
            - `04_api_jobs.json`：后续 API 自动化任务清单。
            - `05_editing_plan.md`：剪辑规则。
            - `06_publish_pack.md`：标题、封面文案、简介、标签。
            - `07_viral_distribution.md`：传播钩子、A/B 测试、海外分发包。

            ## 重新生成

            ```bash
            {command}
            ```

            ## 接 API

            把 API 密钥放到本地 `.env`，不要写进这些 Markdown 文件。把供应商接口文档给 Codex 后，按 `04_api_jobs.json` 接入图片、视频、配音、剪辑或发布适配器。
            """
        ).strip(),
    )


def main() -> int:
    args = parse_args()
    platform = PLATFORM_DEFAULTS[args.platform]
    project = ProjectInput(
        project=args.project,
        platform=args.platform,
        figure=args.figure,
        topic=args.topic,
        style=args.style,
        duration=args.duration or platform["duration"],
        language=args.language,
        output_dir=Path(args.output_dir).expanduser() / slugify(args.project),
        config=Path(args.config).expanduser() if args.config else None,
        env_file=Path(args.env_file).expanduser() if args.env_file else None,
        live=args.live,
    )

    started = time.time()
    load_env(project.env_file)
    config = load_config(project.config)

    rows = storyboard_rows(project)
    script = build_script(project, config)
    project.output_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ["assets/images", "assets/videos", "assets/audio", "exports"]:
        (project.output_dir / subdir).mkdir(parents=True, exist_ok=True)

    write_json(
        project.output_dir / "00_manifest.json",
        {
            "schemaVersion": "1.0",
            "project": project.project,
            "platform": project.platform,
            "figure": project.figure,
            "topic": project.topic,
            "style": project.style,
            "duration": project.duration,
            "language": project.language,
            "live": project.live,
            "createdAt": datetime.now().isoformat(timespec="seconds"),
        },
    )
    write_text(project.output_dir / "01_script.md", script)
    write_storyboard(project.output_dir / "02_storyboard.csv", rows)
    write_text(project.output_dir / "03_prompts.md", build_character_sheet(project) + "\n\n" + build_prompts(project, rows))
    write_json(project.output_dir / "04_api_jobs.json", build_api_jobs(project, rows))
    write_text(project.output_dir / "05_editing_plan.md", build_editing_plan(project))
    write_text(project.output_dir / "06_publish_pack.md", build_publish_pack(project))
    write_text(project.output_dir / "07_viral_distribution.md", build_viral_distribution_pack(project))
    write_readme(project, project.output_dir / "README.md")

    elapsed = time.time() - started
    print(f"Wrote project package: {project.output_dir}")
    print(f"Mode: {'live' if project.live else 'scaffold'}")
    print(f"Elapsed: {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
