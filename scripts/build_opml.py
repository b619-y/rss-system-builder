#!/usr/bin/env python3
"""Validate a topic feed manifest and create portable OPML (no network access)."""

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value.strip()


def build(document):
    if not isinstance(document, dict):
        raise ValueError("Manifest must be a JSON object")
    title = nonempty(document.get("title"), "title")
    feeds = document.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        raise ValueError("feeds must be a nonempty list")
    root = ET.Element("opml", version="2.0")
    ET.SubElement(ET.SubElement(root, "head"), "title").text = title
    body = ET.SubElement(root, "body")
    groups, seen = {}, set()
    for index, feed in enumerate(feeds, 1):
        label = f"feed {index}"
        if not isinstance(feed, dict):
            raise ValueError(f"{label} must be an object")
        name = nonempty(feed.get("title"), f"{label} title")
        category = nonempty(feed.get("category", "Subscriptions"), f"{label} category")
        url = nonempty(feed.get("url"), f"{label} url")
        if any(ch.isspace() or ord(ch) < 32 for ch in url):
            raise ValueError(f"{label} URL must not contain whitespace or controls")
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError(f"{label} requires an HTTP(S) URL with a hostname")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError(f"{label} URL contains credentials; do not export them")
        if url in seen:
            raise ValueError(f"{label} duplicates an earlier feed URL")
        seen.add(url)
        if category not in groups:
            groups[category] = ET.SubElement(body, "outline", text=category, title=category)
        ET.SubElement(groups[category], "outline", type="rss", text=name, title=name, xmlUrl=url)
    ET.indent(root, space="  ")
    payload = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    ET.fromstring(payload)  # Reject illegal XML characters before creating a file.
    return payload, len(feeds), len(groups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
        payload, count, groups = build(document)
        if args.output:
            with args.output.open("xb") as stream:
                stream.write(payload + b"\n")
        print(f"Structure valid: {count} feeds in {groups} categories. Network availability not tested.")
        if args.output:
            print(f"OPML written: {args.output.resolve()}")
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
