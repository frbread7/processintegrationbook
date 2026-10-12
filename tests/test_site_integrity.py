import json
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.duplicate_ids = []
        self.h1_count = 0
        self.h1_text = []
        self.in_h1 = False
        self.html_lang = None
        self.buttons_without_label = []
        self.in_button = False
        self.button_stack = []
        self.inputs = []
        self.label_targets = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_lang = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "label" and attrs.get("for"):
            self.label_targets.add(attrs["for"])
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.duplicate_ids.append(attrs["id"])
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append((tag, attr, attrs[attr]))
        if tag == "button":
            self.button_stack.append({"labelled": bool(attrs.get("aria-label") or attrs.get("title")), "text": ""})
        if tag == "input" and attrs.get("type") not in {"hidden", "submit", "button"}:
            self.inputs.append((attrs.get("id"), attrs.get("aria-label")))

    def handle_data(self, data):
        if self.in_h1:
            self.h1_text.append(data)
        if self.button_stack:
            self.button_stack[-1]["text"] += data.strip()

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "button" and self.button_stack:
            button = self.button_stack.pop()
            if not button["labelled"] and not button["text"]:
                self.buttons_without_label.append(True)


class SiteIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "library-manifest.json").read_text(encoding="utf-8"))
        cls.pages = sorted(SITE.rglob("*.html"))

    def test_renderer_is_current(self):
        run = subprocess.run([sys.executable, str(ROOT / "tools/build_site.py"), "--check"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("routes are current", run.stdout)

    def test_catalog_contract_and_bilingual_chapter_routes(self):
        self.assertEqual(self.manifest["chapterCount"], 13)
        self.assertEqual(len(self.manifest["chapters"]), 13)
        self.assertEqual(self.manifest["languages"], ["en", "ko"])
        self.assertEqual([item["number"] for item in self.manifest["chapters"]], list(range(1, 14)))
        self.assertEqual(len({item["id"] for item in self.manifest["chapters"]}), 13)
        for chapter in self.manifest["chapters"]:
            self.assertTrue(chapter["topics"], chapter["id"])
            for topic in chapter["topics"]:
                english, separator, korean = topic.partition(" / ")
                self.assertTrue(separator and english.strip() and korean.strip(), (chapter["id"], topic))
            for lang in ("en", "ko"):
                relative = chapter["urls"][lang].replace(self.manifest["productionUrl"], "")
                self.assertTrue((SITE / relative).is_file(), relative)
                self.assertTrue(chapter["title"][lang])

    def test_chapter_manifest_titles_are_rendered_and_inputs_have_labels(self):
        for chapter in self.manifest["chapters"]:
            for lang in ("en", "ko"):
                relative = chapter["urls"][lang].replace(self.manifest["productionUrl"], "")
                parsed = PageParser()
                parsed.feed((SITE / relative).read_text(encoding="utf-8"))
                self.assertEqual("".join(parsed.h1_text).strip(), chapter["title"][lang], relative)
        for page in self.pages:
            parsed = PageParser()
            parsed.feed(page.read_text(encoding="utf-8"))
            self.assertTrue(
                all(label or input_id in parsed.label_targets for input_id, label in parsed.inputs),
                page.relative_to(SITE).as_posix(),
            )

    def test_every_internal_link_asset_and_fragment_resolves(self):
        self.assertGreaterEqual(len(self.pages), 34)
        for page in self.pages:
            relative = page.relative_to(SITE).as_posix()
            parsed = PageParser()
            parsed.feed(page.read_text(encoding="utf-8"))
            self.assertFalse(parsed.duplicate_ids, f"{relative}: duplicate ids {parsed.duplicate_ids}")
            self.assertIn(parsed.html_lang, {"en", "ko"}, relative)
            self.assertEqual(parsed.h1_count, 1, relative)
            self.assertFalse(parsed.buttons_without_label, relative)
            base = "https://local.invalid/" + relative
            for tag, attribute, value in parsed.links:
                if value.startswith(("https://", "mailto:", "tel:")):
                    continue
                target = urlsplit(urljoin(base, value))
                if target.netloc != "local.invalid":
                    continue
                route = target.path.lstrip("/")
                if not route or route.endswith("/"):
                    route = route + "index.html"
                target_file = SITE / route
                self.assertTrue(target_file.is_file(), f"{relative}: missing {attribute} {value} -> {route}")
                if target.fragment:
                    target_parser = PageParser()
                    target_parser.feed(target_file.read_text(encoding="utf-8"))
                    self.assertIn(target.fragment, target_parser.ids, f"{relative}: missing anchor {value}")

    def test_language_routes_have_expected_locale_and_project_metadata(self):
        for relative, lang in [("index.html", "en"), ("ko/index.html", "ko"), ("lab.html", "en"), ("ko/lab.html", "ko")]:
            parser = PageParser()
            parser.feed((SITE / relative).read_text(encoding="utf-8"))
            self.assertEqual(parser.html_lang, lang)
        for page in self.pages:
            contents = page.read_text(encoding="utf-8").lower()
            self.assertNotIn("books.euiyun.com", contents)
            self.assertNotIn("cloudflare worker", contents)
            self.assertNotIn("google-analytics", contents)
            self.assertIn("processintegrationbook", contents)

    def test_lab_anchors_and_safe_labels_exist(self):
        for route in ("lab.html", "ko/lab.html"):
            parser = PageParser()
            parser.feed((SITE / route).read_text(encoding="utf-8"))
            for anchor in ("thermal-lab", "dependency-explorer", "integration-review"):
                self.assertIn(anchor, parser.ids)
            html = (SITE / route).read_text(encoding="utf-8")
            self.assertIn("data-concentration-warning=", html)
            self.assertIn("hold-limit-note", html)
        self.assertEqual({item["kind"]["en"] for item in self.manifest["experiments"]}, {
            "Analytically checked, model-limited", "Qualitative constraint map", "Qualitative learning activity"
        })


if __name__ == "__main__":
    unittest.main()
