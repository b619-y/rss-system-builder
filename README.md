# RSS System Builder · 个人主题 RSS 体系搭建

告诉 AI 你的兴趣、研究方向和阅读偏好，搭建适合自己的 RSS 信息订阅体系。

这是供智能体使用的 skill，包含配置指引和 OPML 工具，不是独立阅读器或开箱即用的推送服务。

## 功能

- **主题订阅**：发现并验证 RSS 来源，兼顾领域前沿与具体研究问题。
- **中文阅读**：先看中文标题和摘要，重要文章再按需获取全文。
- **机构全文下载**：按需通过浙大图书馆/WebVPN/Summon 和已登录浏览器获取、验证 PDF 及补充材料。
- **本地翻译**：可选 TranslateGemma 4B + Ollama，将英文翻成简体中文，支持空闲卸载与长文分段。
- **时效筛选**：区分近期动态与历史参考，保留原文、收藏和已读记录。
- **动态关注**：根据用户指定的笔记或当前问题调整精选方向。
- **迁移与通知**：导出 OPML，按需配置跨端同步、Bark 手机通知及 Apple Watch 镜像提醒。

翻译模型、同步服务和定期通知需另行配置；全文获取取决于来源与访问权限，机器翻译需核对专业术语。

## 阅读效果

![MrRSS：分类订阅、文章列表与中文翻译](docs/images/mrrss-demo.png)

经授权展示的真实 MrRSS 阅读截图，包含历史文献，仅作为使用示例。

## Mac 推荐搭配

推荐使用免费开源阅读器 [MrRSS](https://github.com/DevXDojo/MrRSS/blob/main/README_zh.md)：本 skill 组织订阅，MrRSS 管理阅读，可选本地模型提供翻译。

[下载 MrRSS](https://github.com/DevXDojo/MrRSS/releases/latest) · [本地翻译配置](references/local-translation.md)

## 安装与使用

将本仓库安装到智能体的技能目录。Codex 个人目录示例：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/b619-y/rss-system-builder.git ~/.agents/skills/rss-system-builder
```

已有同名目录时不要覆盖。也可把仓库链接交给智能体，请它安装。安装后输入：

```text
使用 $rss-system-builder，根据我的兴趣和研究方向搭建 RSS。
关注主题：[填写主题]
阅读偏好：[语言、设备、预算]
请兼顾领域前沿与近期问题，先验证来源，再配置阅读与翻译。
```

## 详细指南

[Skill 工作流程](SKILL.md) · [浙大论文下载 SOP](references/zju-paper-download-sop.md) · [来源与 OPML](references/manifest.md) · [动态关注与通知](references/adaptive-focus.md) · [阅读与时效](references/reading-and-freshness.md) · [MrRSS 配置](references/mrrss.md)

本项目与 MrRSS、OpenAI、Bark 无隶属关系。请勿上传账号密钥、个人数据库或未发表研究资料。
