# MrRSS implementation notes

These notes describe observed desktop behavior, not a stable public API contract. Inspect the installed version and available source/docs before using endpoints or fields. Do not install or upgrade MrRSS merely to match this reference.

## Prefer app operations

Import OPML and configure existing feeds/rules through the app or its verified local API. A macOS build has used an application-support `MrRSS/rss.db` database and a loopback API, but discover both from the running process; do not assume a username, port or path. Never expose the local API publicly.

Observed endpoints include POST `/api/refresh`, POST `/api/feeds/refresh?id=...`, GET `/api/progress`, and POST `/api/articles/translate` with `article_id`, `title`, `target_language`. Verify method/payload/authentication in the installed build. A `refreshing` response only acknowledges enqueueing. Require successful per-feed completion and persisted article data. A stuck `is_running=true` with empty queues warrants log inspection rather than repeated refreshes.

## Database fallback

Use a database fallback only when necessary within the authorized change. Stop all reader processes first. Create a consistent SQLite backup via the backup API or SQLite `.backup`, including committed WAL data; do not assume copying only the main file is sufficient. Inspect current schema, triggers and foreign keys. Use a transaction, bound parameters and an explicit change set; retain backup and rollback instructions.

Some builds allow nullable `feeds.description` in SQL but scan it into a non-null Go string. Inserting NULL can break listing and refresh for all feeds. App-created records should establish required/default fields. Never mass-normalize unrelated rows to repair a single insertion. Some migration logs mention an unavailable `MD5` SQL function; investigate its actual effect rather than assuming integrity or deduplication is working.

Do not reuse an old source's feed ID for a new query: old articles retain that ID and contaminate the new category. Add a new source and preserve the old one; change old visibility only as authorized. Do not reset hidden/favorite state across whole feed ranges. Save exact affected row IDs and prior values if a batch update is unavoidable.

## Filtering and dates

An observed `rules` setting contains an ordered JSON array with `id`, `name`, `enabled`, `conditions`, `actions`, `position`. Conditions have `id`, `logic`, `negate`, `field`, `operator`, `value`, `values`. Fields include `feed_category`, `article_title`, `article_content`; text regex uses Go regexp. First matching rule wins. Body conditions may use only cached content.

Treat these as candidate semantics: test a mixed batch and a second refresh. A rule appearing saved does not establish correct matching; complex condition evaluation and missing caches can yield surprising results. Do not publish a rule package as verified without observing its effects. Prefer fewer explicit conditions and a review category when reliable behavior cannot be demonstrated.

Hidden feeds can remain in the sidebar and contribute to badges; that does not mean they appear in the main timeline. Check visible items directly. Deduplication may be source-specific, so identical articles from two queries may remain duplicated. One-off hiding is not a persistent deduplication feature.

Some journal feeds omit publication dates; the app may display ingestion time. Verify the underlying feed before calling these “newly published” papers. Historical arXiv search results are a seed library with ongoing updates, not necessarily recent papers.

## Translation and background operation

Observed settings distinguish `language`, `target_language`, `translation_enabled`, `translation_provider`, `translation_trigger_mode` and `translation_only_mode`. Automatic title translation can depend on visible list items; verify nonvisible items separately. The title endpoint does not translate the article body. Full-text extraction can fail independently of RSS refresh.

An inspected build falls back from AI translation to an online translator on AI failure or quota exhaustion. Verify/disable this path when local-only processing is required. A locally configured model alone does not prove local-only operation.

Creating an AI profile does not necessarily select it for translation. Verify the translation feature's profile association and resolve its actual model/endpoint; an unselected local profile can coexist with a legacy cloud-model default. Select only the intended feature's existing profile and retest after refresh. Some inspected refresh paths replace cached translated titles; verify after an actual refresh, not just before it, and do not repeatedly trigger feed updates to refresh the UI.

Inspect the reader's own AI usage counter when local translation suddenly stops. An observed global token cap can trigger online fallback even for a local model. This is not an Ollama model quota. Do not lift a shared cap until checking whether other enabled features use paid services. For an explicitly local-only setup with no paid features, an appropriate adjustment may be possible; preserve the counter, disclose the changed cap and verify the resolved local endpoint. Do not claim all cloud fallback paths are disabled merely because a quota no longer triggers one.

Fixed polling requires the process and appropriate network path to remain available. Closing to tray and quitting are different. Verify scheduler logs and persistence after restart. OS push, cross-device sync, and phone/watch forwarding are additional capabilities, not consequences of enabling polling. Do not change app auto-update preferences unless requested or a specific authorized repair requires it; disclose any such change.
