# Portable source manifest

Use a UTF-8 JSON file with this shape. Additional fields, including topic-profile and verification notes, are retained in the manifest but are not embedded into OPML by the helper.

```json
{
  "title": "My topic subscriptions",
  "profile": {
    "topic": "User supplied topic",
    "include": [],
    "exclude": [],
    "language": "zh",
    "devices": [],
    "freshness": "new entries",
    "sync_requested": false,
    "notifications_requested": false
  },
  "feeds": [
    {
      "title": "arXiv artificial intelligence",
      "category": "Background",
      "url": "https://rss.arxiv.org/rss/cs.AI",
      "verification": {
        "status": "candidate",
        "checked_at": null,
        "entry_count": null,
        "note": "Illustrative candidate; verify before import."
      }
    }
  ]
}
```

The example is a format illustration, not a default subscription. Populate real topics and verified sources for each user. Do not embed credentials, tokens or private server URLs in a shareable manifest/OPML. If a feed requires a secret URL, keep it local and redact it from shared artifacts.

Commands (resolve the script relative to this skill):

```bash
python3 scripts/build_opml.py manifest.json --check
python3 scripts/build_opml.py manifest.json --output subscriptions.opml
```

The builder accepts only nonempty title/category/URL strings and HTTP(S) URLs without embedded usernames or passwords; it rejects exact duplicate feed URLs and refuses to overwrite files. Category defaults to `Subscriptions` when omitted. It escapes XML, preserves source/category order and parses generated XML before writing. URL tokens in query strings are not detected automatically: inspect sharing scope yourself.

For a refresh or migration, export the existing configuration first and generate a new output path. Reader-specific rules, read states, favorites, translations and schedules are separate from OPML.
