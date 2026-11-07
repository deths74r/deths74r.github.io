#!/usr/bin/env python3
"""Validate the rendered site's metadata. Run after Hugo and Pagefind."""
import argparse
from collections import Counter
from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.meta = {}
        self.links = []
        self.times = []
        self.title = ""
        self.schema = []
        self.field = None
        self.buffer = ""
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = attrs.get("name", attrs.get("property", attrs.get("http-equiv")))
            if key:
                self.meta.setdefault(key, []).append(attrs.get("content", ""))
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "time":
            self.times.append(attrs.get("datetime"))
        if tag == "title" or (tag == "script" and attrs.get("type") == "application/ld+json"):
            self.field = tag
            self.buffer = ""

    def handle_data(self, text):
        if self.field:
            self.buffer += text

    def handle_endtag(self, tag):
        if self.field == tag:
            if tag == "title":
                self.title = self.buffer
            else:
                self.schema.append(json.loads(self.buffer))
            self.field = None

    def value(self, name):
        values = self.meta.get(name, [])
        assert len(values) == 1, f"Expected one {name}, found {len(values)}"
        return values[0]


def check_site(root):
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    indexed = {node.findtext("{*}loc"): node for node in sitemap}
    titles, descriptions, canonicals = [], [], []
    articles = {}
    page_count = 0
    for path in sorted(root.rglob("*.html")):
        try:
            page = Page(path.read_text())
            if "refresh" in page.meta:  # Hugo's legacy-URL redirect documents
                continue
            page_count += 1
            assert page.title.strip(), "Missing title"
            desc = page.value("description")
            assert desc.strip() and "<" not in desc, "Missing/plain-text description"
            assert page.value("og:title") == page.value("twitter:title") == page.title
            assert page.value("og:description") == page.value("twitter:description") == desc
            assert page.value("author").strip()
            titles.append(page.title)
            descriptions.append(desc)
            url = page.value("og:url")
            assert url.startswith("https://"), "Non-HTTPS page URL"
            noindex = "noindex" in page.value("robots")
            canonical = [link["href"] for link in page.links if link.get("rel") == "canonical"]
            if path.name == "404.html":
                assert noindex and not canonical and not page.schema
            else:
                assert canonical == [url], "Canonical and social URL disagree"
                canonicals.append(url)
                assert (url in indexed) != noindex, "Sitemap and robots policy disagree"
            image_url = page.value("og:image")
            assert image_url == page.value("twitter:image")
            assert urlsplit(image_url).netloc == urlsplit(url).netloc
            image = root / unquote(urlsplit(image_url).path).lstrip("/")
            assert image.is_file(), "Missing social image"
            width, height = struct.unpack(">II", image.read_bytes()[16:24])
            assert (width, height) == (int(page.value("og:image:width")), int(page.value("og:image:height")))
            assert page.value("og:image:alt") == page.value("twitter:image:alt")
            nodes = [node for graph in page.schema for node in graph.get("@graph", [])]
            posts = [node for node in nodes if node.get("@type") == "BlogPosting"]
            if posts:
                assert len(posts) == 1 and page.value("og:type") == "article"
                post = posts[0]
                assert post["description"] == desc and post["url"] == url
                date = datetime.fromisoformat(post["datePublished"])
                assert date.tzinfo is not None
                assert post["datePublished"] == page.value("article:published_time")
                assert date.date().isoformat() in page.times, "Byline and publication metadata disagree"
                author = next(node for node in nodes if node.get("@id") == post["author"]["@id"])
                assert author["name"] == page.value("author")
                assert author["url"] == page.value("article:author")
                if "dateModified" in post:
                    assert post["dateModified"] == page.value("article:modified_time")
                    assert datetime.fromisoformat(post["dateModified"]) >= date
                else:
                    assert "article:modified_time" not in page.meta
                articles[url] = (date, desc)
            else:
                assert page.value("og:type") == "website"
                assert not any(key.startswith("article:") for key in page.meta)
            for node in nodes:
                if node.get("url") == url and node.get("@type") not in ("WebSite", "Person"):
                    assert node.get("description") == desc
        except (AssertionError, KeyError, ValueError, StopIteration) as exc:
            raise AssertionError(f"{path.relative_to(root)}: {exc}") from exc
    for label, values in [("title", titles), ("description", descriptions), ("canonical", canonicals)]:
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        assert not duplicates, f"Duplicate {label}: {duplicates}"
    assert articles, "No articles checked"
    feed_count = 0
    for path in root.rglob("*.xml"):
        channel = ET.parse(path).find("channel")
        if channel is None:
            continue
        feed_count += 1
        dates = []
        items = channel.findall("item")
        for item in items:
            url = item.findtext("link")
            assert url in articles, f"{path}: non-essay feed item {url}"
            date, desc = articles[url]
            assert parsedate_to_datetime(item.findtext("pubDate")) == date
            assert item.findtext("description") == desc
            assert item.findtext("{http://purl.org/dc/elements/1.1/}creator")
            dates.append(date)
        assert dates == sorted(dates, reverse=True), f"{path}: feed order"
    assert (root / "pagefind/pagefind.js").exists(), "Search index not rebuilt"
    print(f"Metadata OK: {page_count} pages, {len(articles)} essays, {feed_count} feeds; titles, descriptions, canonicals, images, dates, author identities, and indexing policies checked.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="public", type=Path)
    args = parser.parse_args()
    check_site(args.site)
