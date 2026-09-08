# 浙大授权论文全文下载 SOP

RSS 条目只负责发现论文；标题、摘要和 DOI 不能替代全文。用户明确要求获取全文时，按本 SOP 使用用户本人已经登录的浙大图书馆、WebVPN、求是学术搜索/Summon 和出版社会话。只使用合法机构订阅、开放获取或出版社官方入口，不绕过付费墙、验证码、Cloudflare、DRM 或二次认证。

## 总体决策顺序

```text
RSS 条目
  ↓ 提取 DOI、标题、原文链接、发表日期
去重并确认论文身份
  ↓
有明确 OA 直链？ ── 是 → 直接下载 → 验证 → 入库
  ↓ 否
DOI 属于 Elsevier 且已配置官方 TDM 权限？ ── 是 → 走 Elsevier TDM 流程
  ↓ 否/失败
用户已授权的浙大浏览器会话可用？ ── 是 → Summon/WebVPN/出版社浏览器流程
  ↓ 否
记录为待人工认证或未找到授权全文，不寻找非授权镜像
```

优先级不是“能打开网页就算完成”，而是：

1. RSS 条目中的官方全文/OA 链接；
2. 浙大 Summon（求是学术搜索）按 DOI 或精确标题查找 PDF/在线全文入口；
3. WebVPN 或出版社页面完成机构授权；
4. 通过 CDP 在已登录浏览器页面上下文中下载；
5. 若浏览器 PDF 阅读器不暴露字节，点击页面的官方 Download PDF/View PDF，让浏览器正常下载；
6. 校验文件后再交给 MinerU、PDF 解析或翻译流程。

## 浏览器通道：CDP 优先，Edge 作为人工可见回退

### CDP 快速路径

适用于用户已在 Chrome 中登录浙大图书馆/WebVPN，且已允许远程调试的情况。先确认 CDP 代理可用，再打开 Summon 搜索 URL。Summon 是慢速 SPA：导航后等待约 6 秒，最多做 3 次短间隔的链接检查；含 `#!` 的 URL 必须完整编码，避免打开 `about:blank`。

从结果中优先提取非空的 `PDF`、`在线全文`、`Full Text` 或 `View PDF` 链接。打开后，在同一已认证页面上下文执行 `fetch(url, {credentials: "include"})`，读取响应字节并分块写入目标文件；默认检查响应以 `%PDF` 开头。不要读取或导出 cookie、密码、localStorage、session token 或浏览器配置文件。

推荐使用配套脚本（若用户已安装 `zju-literature-downloader`）：

```bash
node scripts/cdp_open_url.mjs --url '<完整 Summon 或出版社 URL>' --wait
node scripts/browser_pdf_downloader.mjs \
  --url '<已授权 PDF URL>' \
  --out '<输出路径>.pdf' --close
```

脚本的工作方式是通过本地 CDP 代理创建/导航标签页，在页面内以当前登录态获取 PDF，再把字节分块传回本地；它不是命令行匿名抓取，也不绕过机构权限。若现有环境没有 CDP 代理，不要为了 RSS 下载临时改全局网络配置。

### Edge/WebVPN 可见回退

以下情况优先回到用户正在使用的 Microsoft Edge/WebVPN：CDP 未连接、需要观察登录、出现 CAS/机构选择、出版社验证、Chrome 原生 PDF viewer 无法被 page-context `fetch` 读取，或目标是 APS。只操作已经确认的窗口和标签页，不依赖 front window/active tab 假设。

回退步骤：从论文落地页点击官方 `Download PDF`/`View PDF`，等待浏览器下载完成，忽略 `.crdownload`/`.download` 临时文件，再按修改时间、文件大小、PDF 签名和标题/DOI 识别新文件。APS 直接访问 `journals.aps.org`，不要经过 ZJU WebVPN 的代理路径。

## 出版商和补充材料

先以文章落地页中的真实链接为准，不凭文件名猜补充材料地址。扫描 `Supporting Information`、`Supplementary`、`Supplemental`、`/doi/suppl/`、`_si_`、`_mmc`、`appendix`、媒体和数据文件。PDF、DOCX、XLSX、ZIP、MP4 等明确属于官方补充材料时逐项下载并记录。

- Science、Nature、PNAS、ACS、ScienceDirect、APS：优先使用现有 Edge/WebVPN 规则；ScienceDirect 的 PDF 必须匹配当前 PII，避免误点参考文献或推荐文章中的 `View PDF`。
- Wiley：从已认证文章页的 `location.origin + /doi/pdfdirect/<doi>?download=true` 获取，避免硬编码错误子域名。
- Springer：机构认证完成后可尝试 `/content/pdf/<doi>.pdf`。
- bioRxiv、Frontiers：优先文章页的官方 PDF；OA 直链仍需核对标题和 PDF 签名。
- ACS：正文和 SI 分开判断；SI 可下载但正文不可访问时记录 `si_only_downloaded`，不能称为全文已下载。
- ScienceDirect：若用户手动完成 `Are you a robot?`/CAS 后点击 `View PDF`，可从新开的 `pdf.sciencedirectassets.com` 临时签名 PDF 标签页用浏览器上下文读取；签名过期时让用户在原文章页重新点击一次，不循环重试。

## 认证和失败处理

遇到 CAS、机构选择、验证码、二维码、短信/OTP、Cloudflare 或出版社人机验证时暂停，告诉用户具体标签页并等待其在浏览器中完成。不得索要密码、验证码、cookie 或 token；只有用户在当前对话明确授权、页面在预期机构域名、且 Chrome 已自动填好凭据并只显示清晰的“登录/确认”按钮时，才可点击一次可见的登录按钮。

每篇论文在 manifest 中保留状态，推荐使用：

```text
downloaded
downloaded_with_si
si_only_downloaded
cas_waiting_user
institutional_login_waiting_user
publisher_verification_waiting_user
sciencedirect_robot_check
retry_after_user_verification
browser_pdf_viewer_fallback_needed
summon_unreachable
url_needs_repair
no_authorized_pdf_found
purchase_required
failed_after_retry
```

一个失败通道只做有限重试；验证完成后从同一标签页继续。Summon 连续无法加载时记录 `summon_unreachable`，改走 DOI 出版社页或已确认的 OA 路径一次，不无限刷新或并发打开大量出版社标签页。普通批次建议 5–10 篇，上限约 15–20 篇并保留清单。

## 验证和 RSS 入库

下载完成不等于文件可信。至少检查：文件存在、大小合理、PDF 前几字节为 `%PDF`、页数大于零、提取文本包含标题/摘要/DOI 或补充材料标题。验证失败时保留文件并标记，不把 HTML 登录页改名为 PDF。

manifest 至少包含：

```text
id title doi year venue status pdf_path si_status si_paths source_url downloaded_at notes
```

RSS 流程应保持原始 RSS 标题、链接、DOI 和发表日期；全文下载、PDF 校验、SI 状态和本地路径写入独立的 manifest 或条目关联字段。只有验证通过后，才进入 MinerU/PDF 文本提取/全文翻译；RSS 中只有标题或摘要时，只能标为摘要阅读，不能显示“全文已获取”或“全文已翻译”。

