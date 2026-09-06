# RSS System Builder · 个人主题 RSS 体系搭建

**告诉 AI 你关心什么，让它帮你搭建、验证和维护一套适合自己的信息订阅体系。**

A reusable agent skill for personalized RSS discovery, verified subscriptions, relevance tuning, translation, and optional research-aware notifications.

它是一套供 Codex 等支持 `SKILL.md` 的智能体读取的工作说明，附带 OPML 生成工具；**不是独立 RSS 阅读器，也不是安装后就会自行运行的推送服务**。你可以换成自己的学科、项目、兴趣、语言和设备，不必照搬示例。

## 效果示例

![MrRSS 中的环境科学、计算机与 AI 订阅，以及中文标题和内容翻译示例](docs/images/mrrss-demo.png)

图：用户提供并授权展示的 MrRSS 实际使用截图。左侧保留环境期刊、计算机与 AI 等广域订阅，中间展示课题相关条目，右侧展示中文机器翻译内容。MrRSS 是本例阅读器，不是本项目开发的界面；截图包含历史文献，不代表所有内容都是近期发表，也不代表全文均可免费获取。机器翻译仍需核对专业术语。

## 这个 skill 能帮你做什么？

| 需求 | 智能体按 skill 执行的工作 | 边界 |
| --- | --- | --- |
| 按主题订阅 | 将研究问题、方法、领域和排除项整理成兴趣档案，寻找官方 RSS/Atom 和检索源 | 不是固定期刊清单；来源要在实际网络中验证 |
| 兼顾精准与广泛 | 保留学科前沿、综合期刊等广域频道，再增加课题专题或排序 | 不默认把非课题文章全部隐藏 |
| 中文阅读 | 区分界面语言、标题、摘要和正文翻译，配置合适的方案并抽查术语 | 不强制 Ollama 或特定模型；可用全文与版权权限有关 |
| 可迁移订阅 | 输出主题档案、验证记录和标准 OPML | OPML 不同步已读、收藏或翻译缓存 |
| 跟随研究进展 | 从用户指定的当前问题/笔记提取临时关注方向，调整排序或专题 | 需要授权资料来源及另行配置定期任务 |
| 手机与手表提醒 | 按需接入 Bark 等渠道，去重、控制条数并测试收件 | 需要设备密钥、通知权限和真实运行的调度器 |
| 已有系统调优 | 检查刷新失败、误匹配和翻译问题，尽量保留已读与收藏 | 不默认更换阅读器、修改全局网络或清空订阅 |

仓库内实际可执行的辅助工具只有 `scripts/build_opml.py` 及其测试。搜索、阅读器配置、翻译与通知接入由使用此 skill 的智能体结合用户环境实施；仓库没有预装模型、账号、同步后端或 Bark 推送程序。

## 安装与使用

需要一个能读取本地 skill 的智能体环境；OPML 工具使用 Python 3.9+ 标准库，不需要第三方 Python 包。RSS 阅读器、翻译服务、通知渠道和智能体本身的费用取决于你的选择，本仓库不提供这些服务或额度。

可以把仓库链接交给支持 skill 安装的智能体，要求安装。也可以手动放入它实际使用的技能目录。当前 Codex 官方文档列出的个人技能目录是 `~/.agents/skills`，项目内为 `.agents/skills`；部分已有环境另有配置目录（例如 `~/.codex/skills`），以你的安装环境为准，避免重复安装。[官方技能目录说明](https://learn.chatgpt.com/zh-Hans/docs/customization/overview)

例如，在支持上述个人目录的 macOS/Linux 环境执行：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/b619-y/rss-system-builder.git ~/.agents/skills/rss-system-builder
```

如果目标已存在，先检查现有版本，不要覆盖。安装后开启新任务，输入：

```text
使用 $rss-system-builder 帮我搭建 RSS 体系。
我关注环境科学前沿、计算机与 AI、Codex/DeepSeek 动态，以及 AI × 环境。
当前课题是铬污染场地修复，但不要只推送与铬直接相关的文章。
请保留 ES&T、Nature 环境相关文章等广域订阅。
我希望中文阅读，优先免费方案，先验证来源，再导入我的阅读器。
```

换个领域也可以：

```text
使用 $rss-system-builder。我关注电池回收、正极直接再生和生命周期评价。
请兼顾高相关论文与材料领域前沿，排除股票行情。
我在 Windows 和 iPhone 阅读，希望同步已读状态；先核实免费方案限制。
```

## 随“最近关注的问题”调整

采用“长期兴趣 + 临时问题”两层结构：长期频道持续提供广度，临时问题影响精选顺序或专题检索。不是每次研究方向略变就删掉原来的订阅。

你可以提供一份自己维护的文件，例如：

```markdown
# 当前研究问题
更新时间：填写日期
长期兴趣：环境科学、计算机与 AI、AI × 环境
最近问题：如何评估地下水污染场地的长期修复效果？
需要的证据：现场案例、监测设计、预测模型及不确定性评价
暂不需要：仅有材料性能、没有场地应用关联的宣传性报道
下次复核：填写日期
```

然后明确授权：

```text
只读取我指定的“当前研究问题.md”，每周一检查是否更新。
据此调整精选排序和专题关键词，保留长期广域频道，不自动删源。
请配置实际定期任务，告诉我运行时间、依赖和验证结果。
```

具体执行规范见 [动态关注与通知](references/adaptive-focus.md)。仅安装 skill 不会读取你的其他聊天、远程服务器或全部笔记，也不会自动创建定时任务。

## Bark / Apple Watch 通知

通知是可选的实施步骤，不随仓库自动启用：安装并授权通知 → 将设备密钥保存在本地私密配置 → 绑定发送端 → 发一条测试 → 用户确认手机和手表收件 → 启用选定的推送时间。

应先将已有文章作为历史基线，只给后续新增内容发送小份摘要；按关注领域平衡条目、去重，无新增不打扰。Bark 服务接受消息不等于手表已收到。Apple Watch 的通知去向与 iPhone 是否锁定、手表是否佩戴解锁及镜像设置有关。[Apple 通知说明](https://support.apple.com/zh-cn/108369) · [Bark 项目](https://github.com/Finb/Bark)

设备密钥不可上传 GitHub；通过通知服务发送的公开文章标题和链接也会经过该服务。默认不要发送未发表课题内容或原始笔记。

## OPML 工具

按 [manifest 格式](references/manifest.md) 准备 `manifest.json`，然后在本仓库目录执行：

```bash
python3 scripts/build_opml.py manifest.json --check
python3 scripts/build_opml.py manifest.json --output subscriptions.opml
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
```

工具检查结构、重复 URL、XML 和 URL 中的用户名密码，按分组生成 OPML，拒绝覆盖文件；**不访问网络，也不能发现所有藏在 URL 查询参数中的密钥**。网络有效性和分享前隐私检查仍需另外完成。

## 文件说明

- [SKILL.md](SKILL.md)：智能体的主工作流程与边界。
- [references/manifest.md](references/manifest.md)：来源清单与 OPML 格式。
- [references/adaptive-focus.md](references/adaptive-focus.md)：近期研究问题、定期更新、通知与隐私约束。
- [references/mrrss.md](references/mrrss.md)：MrRSS 的实测注意事项，使用前须核对版本。
- [scripts/build_opml.py](scripts/build_opml.py)：可独立使用的 OPML 生成器。
- [agents/openai.yaml](agents/openai.yaml)：技能名称及默认调用提示。

本项目与 MrRSS、OpenAI、Bark 和图中期刊无隶属关系。第三方名称、界面和文章内容归各自权利人所有；截图仅用于说明使用效果。请勿将个人数据库、账号配置、通知密钥或未发表研究资料提交到本仓库。
