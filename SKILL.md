---
name: rss-system-builder
description: Build or tune a personalized RSS system from the user's topics, goals, devices and language preferences, including verified feeds, relevance filters, portable OPML, and requested translation, sync or notifications. Use for setting up or retargeting an RSS workflow, not merely explaining RSS or searching for a single article.
---

# Personalized RSS system builder

Turn the user's interests into a working, maintainable reading system. Match their language. A topic alone is enough to start discovery; reuse preferences already given. Do not inherit the example project's topics, machine paths, accounts, proxy ports, reader or model choice.

## Understand the reading goal

Capture a small topic profile: purpose, subject/entities, context or application, methods, positive examples, exclusions, preferred language, devices, budget and desired freshness. Ask only for missing choices that materially change the implementation. Start safe independent discovery while waiting.

When the user references their project, inspect only the supplied or authorized project material and recent relevant documents. Extract research questions, mechanisms and decisions, not just repeated words. Keep private project material and internal names out of public search queries; use general scientific or technical terms. Record unresolved assumptions in the profile.

Separate three capabilities:

- **Refresh:** the reader checks sources for new entries. State whether it requires the app running, an awake computer, network access or a hosted service.
- **Sync:** feeds, read state and favorites agree across devices. OPML transfers subscriptions; it does not provide ongoing state synchronization.
- **Notify:** selected new entries produce alerts through an actual configured delivery channel. A refresh timer is not a push service. Phone/watch notification forwarding needs its own setup and delivery check.

Do not configure delivery, install software or create accounts just because those capabilities are discussed. Follow the user's requested implementation scope and existing authorization. Never claim unattended operation until a persistent mechanism is configured and verified.

## Find and verify sources

Prefer an existing reader that satisfies the user's constraints. When selecting a new reader or model, verify current pricing, free-tier limits, platforms, sync and translation using official sources. Do not assume a local model, Ollama, a paid service or a particular reader is required.

Combine narrow topic/search feeds with relevant primary publishers, organizations or journals. Preserve broad discovery streams when the user wants field awareness; use tested filtering for narrower subsets, not as a reason to hide those streams. Preprints supplement journal coverage; a niche query may contain only older papers. Explain that distinction instead of presenting a historical seed collection as current news.

Verify each candidate using its actual RSS/Atom response in the intended network path, then in the chosen reader. An HTTP 200 containing HTML, login or a challenge is a failure. Inspect channel identity, entry count, item URLs, titles and publication dates. A valid empty feed is different from a connection failure; check publishing cadence before replacing it. Do not turn absent dates into today's publication date.

Prefer official documented feed/search endpoints and bounded polling consistent with provider limits. Recheck niche search results for lexical false positives. For failures, inspect response and application logs, then make evidence-based scoped retries. Use an existing authorized per-app proxy if needed; never invent a proxy address, disable TLS checks, bypass access controls or change global networking as an RSS default. Report unresolved sources individually.

Keep a source manifest with `title`, `category`, `url`, provider, verification date, status, returned entry count and relevance notes. Generate portable OPML with `scripts/build_opml.py`; see [references/manifest.md](references/manifest.md). This helper checks structure only and cannot certify network availability.

## Design and calibrate relevance

Distinguish direct topic matches from transferable methods and broader background. A useful inclusion usually combines subject **and** application/context; method words such as AI, redox, optimization or life-cycle assessment alone are often too broad. Exclusions should follow the user's objective, not assumptions about an entire discipline.

Before enabling rules, sample real entries across proposed categories: obvious positives, plausible method papers and misleading keyword matches. Explain why representative items were retained or excluded. Match title and abstract when reliably available; full publisher pages may contain unrelated recommendations, references or navigation. Strip markup where supported. Missing abstracts are unknown, not evidence of irrelevance.

Test the reader's actual AND/OR/NOT semantics, first-match behavior, regex dialect, cache availability and repeat-run behavior. Do not translate an abstract Boolean expression into an untested complex rule. Prefer small rules or a scored review queue when native semantics cannot express the intent reliably. First rule wins may prevent later tagging/hiding; verify the complete rule order with a mixed batch and again after refresh.

Favor reversible categories, labels or review queues. Do not silently remove existing feeds, hide broad areas of interest, clear favorites/read state or reuse an existing feed ID for a different source. Preserve user-curated state. If approved filtering hides entries, explain the recovery path and possible false negatives. Automatic favorites are optional; avoid mixing machine-selected items into personal favorites without making that choice clear.

Deduplicate using DOI, stable article ID or canonical URL first; normalized title is a fallback. Keep a record of which copy survives. Do not claim future automatic deduplication based on a one-time cleanup.

When the user wants recommendations to follow recent research questions or notes, read [references/adaptive-focus.md](references/adaptive-focus.md). Keep a stable interest profile plus an explicitly sourced, time-limited focus overlay. A skill alone does not periodically read notes or send notifications.

## Implement and translate

Prefer documented app APIs, imports and UI over direct database edits. Read [references/mrrss.md](references/mrrss.md) only when operating MrRSS; verify the installed version rather than assuming that reference's endpoint/schema details still apply.

For Chinese or other target-language reading, separate UI language, title translation, abstract translation and full-text availability. RSS often contains only a title or abstract; translating that is not translating the full paper. Keep original titles, links and identifiers accessible.

When the user wants abstract-first triage or separate recent updates from historical research, read [references/reading-and-freshness.md](references/reading-and-freshness.md). Keep full-text retrieval on demand, preserve historical references, and distinguish publication date from discovery time when selecting recent digests.

Choose translation according to hardware, privacy, speed and budget. Check measured disk use, active memory and idle unloading rather than assuming a model size is optimal. Do not silently fall back from a local model to a cloud translator when local-only processing is intended. Inspect the reader's fallback behavior.

For lightweight local English-to-Simplified-Chinese translation, read [references/local-translation.md](references/local-translation.md). It provides an optional TranslateGemma 4B / Ollama recipe, a public-text smoke test, memory controls and reader integration checks. Reuse an existing compatible local model where appropriate; do not download models or change running services just because this reference is loaded.

Create a short domain glossary and check a few real titles, including chemical names, species, abbreviations and technical concepts. Fluent translation can still be wrong: chromate ≠ dichromate, barite ≠ gypsum, ryegrass ≠ oats, and global sensitivity ≠ geographic global scale. If quality is insufficient, correct verified cached translations or improve the prompt/model with a retest; keep the limitation explicit. Do not label machine output as reviewed scientific translation.

## Verify and hand over

Perform a real refresh and inspect per-source success, counts and logs; clicking a button or receiving an accepted response is not completion. Compare the visible list with saved rules and check a representative translated item. Verify existing subscriptions and saved state survive. Do not alter unrelated software update settings as a standard setup step.

Deliver the topic profile, source manifest, OPML and any reader-specific rules. Report separately: verified sources, currently visible items, translated titles/abstracts, configured refresh interval, sync status and notification status. State measured results without invented precision metrics. Give a short recovery/tuning instruction and unresolved limitations. If access is unavailable, deliver an importable, validated package and explicitly say what was not installed or tested.

Example invocation: “Use $rss-system-builder to build a free RSS system for battery recycling, focusing on direct cathode regeneration and process LCA. I read on iPhone and Windows, want Chinese titles and synced read status, and want to exclude stock-market news.”
