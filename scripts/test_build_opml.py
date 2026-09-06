"""Behavioral checks for portable export; never touch the user's reader."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from build_opml import build


class ExportTests(unittest.TestCase):
    def manifest(self):
        return {"title": "研究 & 技术", "feeds": [
            {"title": "A < B", "category": "中文 & English",
             "url": "https://example.org/feed?q=soil&lang=en"},
            {"title": "Methods", "category": "中文 & English",
             "url": "https://example.org/methods"},
        ]}

    def test_xml_preserves_text_urls_and_grouping(self):
        payload, count, groups = build(self.manifest())
        root = ET.fromstring(payload)
        self.assertEqual((count, groups), (2, 1))
        self.assertEqual(root.findtext("head/title"), "研究 & 技术")
        entries = root.findall("body/outline/outline")
        self.assertEqual(entries[0].get("title"), "A < B")
        self.assertEqual(entries[0].get("xmlUrl"), self.manifest()["feeds"][0]["url"])

    def test_rejects_duplicate_and_unsafe_urls(self):
        for url in ("file:///tmp/feed", "https://user:secret@example.org/feed",
                    "https:///feed", "https://example.org/a b",
                    self.manifest()["feeds"][0]["url"]):
            with self.subTest(url=url):
                document = self.manifest()
                document["feeds"][1]["url"] = url
                with self.assertRaises(ValueError):
                    build(document)

    def test_rejects_invalid_manifest_and_xml(self):
        for document in ([], {}, {"title": "t", "feeds": []},
                         {"title": "t", "feeds": [False]}):
            with self.assertRaises(ValueError):
                build(document)
        document = self.manifest()
        document["title"] = "bad\x00title"
        with self.assertRaises(ET.ParseError):
            build(document)

    def test_cli_does_not_overwrite(self):
        script = Path(__file__).with_name("build_opml.py")
        with tempfile.TemporaryDirectory(prefix="rss-skill-test-") as work:
            manifest = Path(work) / "manifest.json"
            output = Path(work) / "subscriptions.opml"
            manifest.write_text(json.dumps(self.manifest()), encoding="utf-8")
            command = [sys.executable, str(script), str(manifest)]
            checked = subprocess.run(command + ["--check"], capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            first = subprocess.run(command + ["--output", str(output)], capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            second = subprocess.run(command + ["--output", str(output)], capture_output=True)
            self.assertEqual(second.returncode, 1)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
