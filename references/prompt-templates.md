# Prompt Templates

Use this reference when producing scripts, character sheets, image prompts, video prompts, voice direction, covers, or title variants.

## Fact Check Prompt

```text
你是历史内容审稿人。请检查下面脚本，把内容分成三类：
1. 可确认史实
2. 主流解释或合理推断
3. 艺术化演绎或需要改写的内容

要求：指出可能争议点，给出更稳妥表达，避免把野史、演义、传说写成确定事实。
脚本：
【粘贴脚本】
```

## Script Prompt

```text
你是历史动画短视频编剧。请围绕【人物】的【关键选择】写一条【平台】【时长】短视频脚本。

结构：
1. 前 3 秒用一个反常识问题或危险瞬间开头
2. 一句话交代时代和人物处境
3. 展示冲突为什么不可回避
4. 写出人物做出的选择
5. 写出选择带来的代价或后果
6. 结尾留一句有余味的话或评论问题

要求：
- 不写百科腔
- 旁白短句，适合口播
- 事实和演绎分开标注
- 不使用影视剧台词或现代流行梗
```

## Viral Rewrite Prompt

```text
你是短视频传播编辑。请把下面历史人物动画脚本改成更适合快速传播的版本。

目标：
- 前 1 秒有视觉冲击或反常识字幕
- 前 3 秒必须打开悬念
- 每 2-4 秒有一次信息或画面变化
- 背景交代不超过一句
- 结尾制造两边都能争的评论问题
- 保留事实边界，不能把推断写成确定史实

输出：
1. 传播钩子评分，满分 10 分
2. 改写后的 45-75 秒脚本
3. 5 个标题：好奇型、冲突型、情绪型、反转型、搜索型
4. 3 个封面文案
5. 3 个第一句开场
6. 2 个结尾：评论争议版、下一集悬念版

原脚本：
【粘贴脚本】
```

## Character Sheet Prompt

```text
为历史人物【人物】创建 AI 动画角色设定表。

输出：
- 年龄段：
- 体型：
- 脸型和五官：
- 发型/头饰：
- 服装：
- 主色：
- 标志物：
- 表情范围：
- 镜头语言：
- 禁止元素：

风格：【电影感/水墨/漫画/纪录片/剪纸】
时代：【朝代或地区】
要求：适合后续多镜头复用，避免现代服饰、现代建筑、错误文字和夸张奇幻元素。
```

## Image Prompt Template

```text
【角色设定摘要】, 【时代地点】, 【情绪】, 【动作】,
【镜头类型】, 【构图】, 【光线】, 【天气/环境】,
historical animation still, consistent character, high detail,
【指定风格】, no modern objects, no extra fingers, no text, no watermark
```

Example:

```text
middle-aged Chinese emperor with sharp eyes, black and gold robe, Qin dynasty palace,
standing beside a candlelit map, tense and silent, medium close-up, low key lighting,
cinematic historical animation still, consistent character, high detail,
no modern objects, no extra fingers, no text, no watermark
```

## Video Prompt Template

```text
Use the reference image as the first frame. Generate a 4-6 second shot:
the character 【simple action】, facial expression changes from 【A】 to 【B】,
camera 【slow push-in / slight pan / handheld documentary movement】,
background 【one subtle motion: candle flicker, flags moving, dust, rain】.
Keep face, clothing, age, and scene consistent. Do not add new characters. No text.
```

## Voice Direction

```text
旁白风格：低速、克制、有悬念，不要夸张播音腔。
情绪曲线：开头压低声音，中段加快一点，关键选择处停顿，结尾收住。
禁忌：不要喊麦、不要过度悲壮、不要像广告配音。
```

## Cover And Title Prompt

```text
请为这条历史人物动画短视频生成 10 个标题和 5 个封面文案。

要求：
- 标题 12-22 个字
- 有冲突、选择、代价或反常识
- 不造谣，不夸大确定性
- 封面文案不超过 10 个字
- 输出每个标题对应的受众心理

视频主题：
【粘贴主题】
```

## Cross-Platform Rewrite Prompt

```text
请把同一条历史人物动画视频改写成海外平台分发包。

平台：
- YouTube Shorts
- TikTok
- Instagram Reels
- Facebook Reels
- Snapchat Spotlight
- Pinterest
- X

要求：
- 每个平台给 1 个标题、1 个开头字幕、1 个简介/Caption、1 个结尾互动问题
- YouTube Shorts 偏搜索和系列
- TikTok 偏反差和评论
- Instagram Reels 偏视觉和封面
- Facebook Reels 偏清晰叙事和可分享
- Snapchat Spotlight 偏快节奏
- Pinterest 偏可收藏和常青搜索
- X 偏争议观点 + 资料补充
- 英文内容要自然改写，不要直译中文

视频主题：
【粘贴主题】
```

## Viral Audit Prompt

```text
请审查这条历史人物动画视频是否具备传播性。

按 0-10 分打分：
- 前 1 秒停留
- 前 3 秒悬念
- 画面变化密度
- 情绪强度
- 反常识程度
- 评论诱因
- 收藏/转发理由
- 历史可信度

输出：
1. 总分
2. 最大流失点
3. 必改 3 处
4. 可测试的 A/B 变量

脚本和分镜：
【粘贴内容】
```

## Negative Prompt Bank

Use for visual generation when needed:

```text
modern clothes, modern buildings, guns, cars, neon signs, wrong dynasty costume,
text, subtitles, watermark, logo, deformed hands, extra fingers, duplicate face,
face changing, inconsistent clothing, fantasy armor, plastic skin, overexposed
```
