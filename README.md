# RSS System Builder · 个人主题 RSS 体系搭建

根据你的兴趣、研究方向和阅读偏好，帮助智能体搭建个性化 RSS 订阅体系。

## 功能

- **主题订阅**：发现并验证 RSS 来源，兼顾领域前沿与具体研究问题。
- **中文阅读**：先看中文标题和摘要，重要文章再按需获取全文。
- **全文获取**：按需通过开放来源或已授权的机构访问获取、验证论文 PDF 及补充材料。
- **本地翻译**：可选轻量模型 TranslateGemma 4B + Ollama，将英文翻成简体中文。
- **时效筛选**：区分近期动态与历史参考，保留原文、收藏和已读记录。
- **动态关注**：根据用户指定的笔记或当前问题调整精选方向。
- **迁移与通知**：导出 OPML，按需配置跨端同步、Bark 手机通知及 Apple Watch 镜像提醒。

这是配置型 skill，不是独立阅读器。翻译、同步和定期通知需另行配置；全文受访问权限限制，专业术语需核对。

## 阅读效果

![MrRSS：分类订阅、文章列表与中文翻译](docs/images/mrrss-demo.png)

经授权展示的真实 MrRSS 阅读截图，包含历史文献，仅作为使用示例。

## Mac 推荐搭配

推荐使用免费开源阅读器 [MrRSS](https://github.com/DevXDojo/MrRSS/blob/main/README_zh.md)：本 skill 组织订阅，MrRSS 管理阅读，可选本地模型提供翻译。

[下载 MrRSS](https://github.com/DevXDojo/MrRSS/releases/latest) · [本地翻译配置](references/local-translation.md)

## 使用与指南

将仓库链接交给智能体安装，然后使用 `$rss-system-builder`，说明你的关注主题、语言和设备偏好即可。

[Skill 工作流程](SKILL.md) · [浙大论文下载 SOP](references/zju-paper-download-sop.md) · [来源与 OPML](references/manifest.md) · [动态关注与通知](references/adaptive-focus.md) · [阅读与时效](references/reading-and-freshness.md) · [MrRSS 配置](references/mrrss.md)

本项目与 MrRSS、OpenAI、Bark 无隶属关系。请勿上传账号密钥、个人数据库或未发表研究资料。
