#!/usr/bin/env python3
"""Generate a one-click historical AI animation channel plan."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from textwrap import dedent


PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "ratio": "9:16",
        "duration": "45-75 秒",
        "cadence": "每周 5-7 条",
        "note": "强钩子、强反差、前三秒必须有悬念或冲突。",
    },
    "bilibili": {
        "name": "B站",
        "ratio": "16:9 或 9:16",
        "duration": "90-240 秒",
        "cadence": "每周 2-4 条",
        "note": "允许更完整叙事，标题和封面要突出知识增量。",
    },
    "xiaohongshu": {
        "name": "小红书",
        "ratio": "3:4 或 9:16",
        "duration": "30-75 秒",
        "cadence": "每周 4-6 条",
        "note": "封面要像图文笔记，标题偏情绪价值和冷知识。",
    },
    "youtube": {
        "name": "YouTube Shorts",
        "ratio": "9:16",
        "duration": "45-60 秒",
        "cadence": "每周 5-7 条",
        "note": "适合系列化英文或双语内容，注意素材版权和 AI disclosure。",
    },
    "tiktok": {
        "name": "TikTok",
        "ratio": "9:16",
        "duration": "35-60 秒",
        "cadence": "每周 5-7 条",
        "note": "节奏更快，适合强戏剧化、视觉冲击和英文字幕。",
    },
    "instagram": {
        "name": "Instagram Reels",
        "ratio": "9:16",
        "duration": "30-60 秒",
        "cadence": "每周 4-7 条",
        "note": "封面和主页网格很重要，适合电影感视觉、人物金句和系列化 Reels。",
    },
    "facebook": {
        "name": "Facebook Reels",
        "ratio": "9:16",
        "duration": "45-90 秒",
        "cadence": "每周 4-7 条",
        "note": "适合更清晰的叙事、更熟悉的人物和可分享的道德困境。",
    },
    "snapchat": {
        "name": "Snapchat Spotlight",
        "ratio": "9:16",
        "duration": "15-45 秒",
        "cadence": "每周 5-10 条",
        "note": "节奏要更快，字幕更短，优先视觉冲击和对象钩子。",
    },
    "pinterest": {
        "name": "Pinterest",
        "ratio": "9:16 或 2:3",
        "duration": "15-60 秒",
        "cadence": "每周 3-5 条",
        "note": "适合常青搜索、封面图、时间线、服饰和历史美学收藏。",
    },
    "x": {
        "name": "X",
        "ratio": "9:16 或 16:9",
        "duration": "30-90 秒",
        "cadence": "每周 3-7 条",
        "note": "适合视频加短 thread，用争议观点和资料补充带讨论。",
    },
}

TOOLS = {
    "free": {
        "research": "免费大模型 + 公开资料交叉核对",
        "script": "DeepSeek/Kimi/豆包/ChatGPT 免费额度",
        "image": "即梦/通义万相/本地 Stable Diffusion",
        "video": "即梦/可灵/海螺等免费额度轮换",
        "voice": "剪映/CapCut 内置配音或系统 TTS",
        "edit": "剪映/CapCut 免费版",
        "rule": "不先付费，用免费额度验证 20 条内容后再订阅。",
    },
    "low": {
        "research": "1 个主力大模型 + 公开资料核验",
        "script": "DeepSeek/Kimi/ChatGPT 选择一个稳定方案",
        "image": "即梦/通义万相/Liblib/Leonardo 任选一个主工具",
        "video": "可灵/即梦/海螺优先，海外账号可备 Runway/Pika/Luma",
        "voice": "剪映配音、ElevenLabs 或国内 TTS 低档套餐",
        "edit": "剪映专业版或 CapCut Pro，二选一",
        "rule": "低预算只固定 1 个视频工具 + 1 个剪辑工具，其他用免费额度补位。",
    },
    "pro": {
        "research": "主力大模型 + 资料库 + 事实核验流程",
        "script": "ChatGPT/Claude/DeepSeek 中选择最适合长文本的一款",
        "image": "Midjourney/Leonardo/Stable Diffusion 工作流",
        "video": "可灵/Runway/Luma/Pika 组合测试，保留最稳的一款",
        "voice": "ElevenLabs/专业 TTS + 声音风格库",
        "edit": "CapCut/剪映 + DaVinci Resolve",
        "rule": "为稳定出片付费，但每月复盘每个工具是否贡献产出。",
    },
    "team": {
        "research": "资料整理、脚本、视觉、剪辑分工",
        "script": "共享提示词库 + 审稿清单",
        "image": "统一角色设定表 + 批量出图",
        "video": "固定镜头模板 + 多工具并行",
        "voice": "固定旁白音色 + 人工审听",
        "edit": "统一工程模板和封面模板",
        "rule": "团队阶段重点是标准化交付，不是不断换工具。",
    },
}

STYLE_GUIDES = {
    "cinematic": "电影感写实、低饱和、强光影、近景表情和大场面交替",
    "ink": "水墨国风、留白、纸张纹理、缓慢推拉镜头",
    "anime": "动画番剧感、清晰轮廓、情绪夸张、动作更明确",
    "documentary": "纪录片质感、历史插画、地图、文献、低调旁白",
    "comic": "漫画分格、速度线、文字拟声、强反差表情",
    "paper-cut": "剪纸皮影、侧面人物、舞台式运动、民俗色彩",
}

DEFAULT_FIGURES = [
    ("秦始皇", "统一之后，他最害怕的不是六国余孽"),
    ("霍去病", "少年将军为什么能打到匈奴腹地"),
    ("诸葛亮", "他真正的孤独，不在空城计"),
    ("李世民", "玄武门之后，他如何面对史书"),
    ("武则天", "她登基前最危险的一次选择"),
    ("岳飞", "十二道金牌背后的权力困局"),
    ("张居正", "改革成功后，为什么身后崩塌"),
    ("苏轼", "被贬之后，他如何把人生改写"),
    ("王阳明", "龙场悟道前，他几乎被现实击穿"),
    ("林则徐", "禁烟之后，他看到的真正危机"),
]

WORLD_FIGURES = [
    ("凯撒", "他跨过卢比孔河时，已经没有退路"),
    ("克娄巴特拉", "她不是美貌传说，而是最后的政治玩家"),
    ("拿破仑", "滑铁卢之前，胜利惯性如何反噬他"),
    ("贞德", "一个少女如何让法国重新相信自己"),
    ("林肯", "废奴之前，他面对的是撕裂的国家"),
    ("伊丽莎白一世", "她为什么把婚姻变成政治武器"),
    ("丘吉尔", "至暗时刻，他如何让恐惧变成语言"),
    ("甘地", "非暴力背后，是极强的组织能力"),
    ("特斯拉", "天才为什么输给了商业世界"),
    ("曼德拉", "二十七年监禁如何改变一个人"),
]

WOMEN_FIGURES = [
    ("妇好", "她不是王后陪衬，而是能领兵的将军"),
    ("武则天", "她最强的能力不是狠，而是等待"),
    ("上官婉儿", "她在权力夹缝中写字，也写命运"),
    ("李清照", "南渡之后，她失去的不只是爱情"),
    ("梁红玉", "战鼓响起时，她站在了时代前面"),
    ("孝庄太后", "她如何在乱局里押中未来皇帝"),
    ("慈禧", "她的每个选择都被时代放大"),
    ("秋瑾", "她为什么决定把自己推向风暴"),
    ("宋庆龄", "她的一生都在选择更难的路"),
    ("居里夫人", "她付出的代价远高于奖章本身"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a customized historical AI animation video channel plan."
    )
    parser.add_argument("--platform", default="douyin", choices=sorted(PLATFORMS))
    parser.add_argument("--budget", default="low", choices=sorted(TOOLS))
    parser.add_argument("--niche", default="中国历史人物高光转折")
    parser.add_argument("--audience", default="18-35 岁，对历史有兴趣但不想看长课的人")
    parser.add_argument("--style", default="cinematic", choices=sorted(STYLE_GUIDES))
    parser.add_argument("--duration", default="")
    parser.add_argument("--cadence", default="")
    parser.add_argument("--language", default="中文")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def pick_figures(niche: str) -> list[tuple[str, str]]:
    lowered = niche.lower()
    if "世界" in niche or "海外" in niche or "world" in lowered:
        return WORLD_FIGURES
    if "女性" in niche or "女人" in niche or "女" in niche:
        return WOMEN_FIGURES
    return DEFAULT_FIGURES


def topic_rows(figures: list[tuple[str, str]], duration: str) -> str:
    rows = []
    for index, (figure, hook) in enumerate(figures, 1):
        rows.append(
            f"{index}. 《{hook}》 - 人物：{figure} - 冲突：选择/代价/反转 - 钩子：错觉反转 - 视觉：近景表情 + 标志性物件 - 时长：{duration}"
        )
    return "\n".join(rows)


def global_platform_rows() -> str:
    rows = [
        ("YouTube Shorts", "搜索 + 系列沉淀", "45-75 秒", "英文字幕/英文配音都值得测"),
        ("TikTok", "最快验证选题", "35-60 秒", "更强反差、更短背景"),
        ("Instagram Reels", "视觉审美和主页资产", "30-60 秒", "封面统一，字幕干净"),
        ("Facebook Reels", "广泛年龄层分享", "45-90 秒", "叙事更直白，少用梗"),
        ("Snapchat Spotlight", "年轻用户快节奏实验", "15-45 秒", "对象钩子和快速剪辑"),
        ("Pinterest", "常青搜索和收藏", "15-60 秒", "封面、时间线、历史美学"),
        ("X", "争议讨论和外链", "30-90 秒", "视频 + 资料 thread"),
    ]
    return "\n".join(f"- {name}：{role}；建议 {duration}；改写重点：{note}。" for name, role, duration, note in rows)


def make_plan(args: argparse.Namespace) -> str:
    platform = PLATFORMS[args.platform]
    tools = TOOLS[args.budget]
    duration = args.duration or platform["duration"]
    cadence = args.cadence or platform["cadence"]
    figures = pick_figures(args.niche)
    first_figure, first_hook = figures[0]
    today = date.today().isoformat()

    return dedent(
        f"""
        # 历史人物 AI 动画视频账号定制包

        生成日期：{today}

        ## 1. 账号定位

        - 平台：{platform["name"]}，画幅 {platform["ratio"]}，建议时长 {duration}
        - 细分方向：{args.niche}
        - 目标观众：{args.audience}
        - 内容承诺：用动画还原历史人物的关键选择，让观众在 1 分钟内看懂一个人的命运转折。
        - 差异化：不做流水账，不堆百科信息，只讲“一个人物 + 一个危险选择 + 一个后果”。
        - 视觉风格：{STYLE_GUIDES[args.style]}
        - 更新频率：{cadence}
        - 平台提醒：{platform["note"]}
        - 传播原则：先制造“我以前理解错了”的停留，再用事实和代价支撑，最后用两边都能争的问题引导评论。

        ## 2. 内容栏目

        - 人生转折点：讲人物做出不可逆选择的那一刻。
        - 被误解的人：用反常识角度重讲大众熟悉人物。
        - 最后一夜：用临终、战败、被贬、流放前夜制造情绪张力。
        - 如果他没这么选：用历史假设开头，但正文回到史实。
        - 一句话改变命运：围绕奏章、诏书、遗言、书信展开。

        ## 3. 病毒式传播结构

        - 0-1 秒：画面先给冲突，不先打招呼。
        - 1-3 秒：一句反常识钩子，例如“历史记住他赢了，却忘了他赢后的代价。”
        - 3-8 秒：只交代一个背景，不讲生平。
        - 8-40 秒：人物被迫选择，镜头每 2-4 秒变化一次。
        - 40-60 秒：揭示代价，用对象或场景收束。
        - 最后 3 秒：丢出争议问题，例如“这是果断，还是赌徒式冒险？”

        标题 A/B：
        - 好奇型：《{first_figure}真正害怕的不是敌人》
        - 冲突型：《他赢了，却从这里开始失控》
        - 情绪型：《这一步之后，他再也回不了头》
        - 反转型：《历史记住了胜利，却漏掉了代价》
        - 搜索型：《{first_figure}关键选择：胜利背后的代价》

        封面 A/B：
        - 没有退路
        - 赢后的代价
        - 他敢吗

        ## 4. 国外适合发布的平台

        {global_platform_rows()}

        优先级建议：先发 YouTube Shorts + TikTok + Instagram Reels；有余力再同步 Facebook Reels、Pinterest、X；Snapchat Spotlight 用来测试快节奏短版本。

        ## 5. 最具性价比工具栈

        - 资料和核验：{tools["research"]}
        - 脚本：{tools["script"]}
        - 出图：{tools["image"]}
        - 图生视频/文生视频：{tools["video"]}
        - 配音：{tools["voice"]}
        - 剪辑字幕：{tools["edit"]}
        - 预算规则：{tools["rule"]}
        - 付费前动作：先做 20 条样片，统计完播率、收藏率、评论率，再只为瓶颈工具付费。价格和额度变化很快，订阅前核对官方价格。

        ## 6. 标准生产 SOP

        1. 定题：人物 + 冲突 + 反转，标题先写 5 个，封面先写 3 个。
        2. 核验：把事实分成“确定史实、主流说法、艺术化表达”。
        3. 写脚本：前三秒抛问题，中段讲选择，结尾给争议问题。
        4. 分镜：6-10 个镜头，避免每句旁白都生成新场景。
        5. 角色设定：固定年龄、服饰、脸型、发型、色彩和镜头语言。
        6. 出图：先出角色定妆，再出关键场景。
        7. 动画：每个镜头只描述一个动作，减少模型漂移。
        8. 配音：稳、克制、有悬念，不要播音腔过满。
        9. 剪辑：强字幕、弱转场、每 2-4 秒有视觉变化。
        10. 发布复盘：24 小时看完播率，72 小时看收藏和评论。

        ## 7. 通用提示词

        脚本提示词：
        “你是历史短视频编剧和传播编辑。请围绕【人物】和【关键选择】写一个 {duration} 的短视频脚本。结构：1 秒视觉冲击、3 秒反常识钩子、背景一句话、冲突升级、关键选择、代价、评论争议问题。要求：事实和演绎分开，不写百科腔，旁白适合口播，每 2-4 秒有一个画面变化。”

        角色设定提示词：
        “为【人物】设计 AI 动画角色设定表：年龄、体型、脸型、发型、服饰、配色、时代符号、表情范围、负面限制。风格：{STYLE_GUIDES[args.style]}。要求后续镜头可复用，避免现代元素。”

        图像提示词模板：
        “【人物设定】，【朝代/地点】，【情绪】，【动作】，【镜头】，【光线】，【构图】，【风格】，historical animation still, consistent character, high detail, no modern objects, no extra fingers, no text”

        视频提示词模板：
        “基于参考图生成 4-6 秒镜头：人物【动作】，镜头【推近/横移/轻微摇镜】，环境【风/烛火/尘土】轻微运动，表情从【A】到【B】，保持角色一致，不改变服饰，不新增人物。”

        ## 8. 首批 10 条选题

        {topic_rows(figures, duration)}

        ## 9. 第一条完整样片方案

        标题备选：
        - 《{first_hook}》
        - 《{first_figure}真正害怕的那一刻》
        - 《如果你是{first_figure}，这一局怎么选？》

        旁白脚本：
        “历史记住了{first_figure}的胜利，却很少讲他赢完之后失去了什么。那一刻，他面对的不是一个敌人，而是一条不能回头的路。退一步，他会失去已经拿到的一切；进一步，他必须承担所有人的恐惧和反对。真正改变历史的，不是胜利后的欢呼，而是他按下决定前的几秒钟。如果你站在他的位置，这是果断，还是赌徒式冒险？”

        分镜：
        1. 黑场字幕 + 鼓点：抛出“他最害怕的不是敌人”。
        2. 人物近景：烛光下沉默，眼神压住情绪。
        3. 地图/宫殿/战场环境：展示局势压力。
        4. 手部特写：按住诏书、剑柄、竹简或战报。
        5. 群像远景：臣子、士兵或百姓等待决定。
        6. 人物转身：做出选择。
        7. 大场面：风、尘土、旗帜或宫门打开。
        8. 结尾近景：字幕点题“真正改变历史的，是选择前的那一秒。”

        ## 10. 30 天执行计划

        - 第 1-2 天：确定账号名、头像风格、简介、封面模板。
        - 第 3-5 天：批量写 20 个选题，只保留最有冲突的 10 个。
        - 第 6-10 天：完成 10 条脚本和角色设定表。
        - 第 11-18 天：完成首批 5 条视频，统一字幕和封面样式。
        - 第 19-25 天：日更测试，记录完播率、点赞率、收藏率、评论关键词。
        - 第 26-30 天：复盘标题、钩子、视觉风格，放大表现最好的栏目。

        ## 11. 合规和风险

        - 明确 AI 生成或 AI 辅助，遵守平台标识要求。
        - 不把野史、传说、演义写成确定史实。
        - 避免使用影视剧截图、未授权音乐和他人画作风格指名复刻。
        - 涉及民族、宗教、战争、现实政治类内容时，降低煽动性表达。

        ## 12. 复盘指标

        - 完播率低：前三秒不够强，或镜头太慢。
        - 点赞低：情绪不够明确，人物选择没有代入感。
        - 收藏低：知识增量不足，缺少反常识。
        - 评论低：结尾没有留下争议问题。
        - 涨粉低：账号栏目不稳定，观众不知道关注后还能看什么。
        - 转发低：没有“我想发给别人看”的反常识或情绪点。
        """
    ).strip().replace("\n        ", "\n") + "\n"


def main() -> None:
    args = parse_args()
    plan = make_plan(args)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(plan, encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(plan)


if __name__ == "__main__":
    main()
