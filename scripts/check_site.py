"""Validate built static output without fetching the unpublished custom domain."""

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import struct
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ORIGIN = "https://kiss.i-pp.co.jp"
ROUTES = ("", "philosophy/", "products/", "products/aceis/", "roadmap/", "docs/", "contributing/")
ASSETS = {
    "project-kiss.png": ("a068c475fe999657d3b8de50c59fd33caca8ade74e88dd36954b48ff286253c9", (800, 840)),
    "project-aceis.png": ("91432ca2c89cfcc318865a8908916cdd5b43d9764bde6bd1cda1830a4e1bd088", (896, 856)),
}


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.errors = []
        self.references = []
        self.alternates = {}
        self.canonical = []
        self.lang = None
        self.h1_count = 0
        self.main_count = 0
        self.has_title = False
        self.has_description = False
        self.has_viewport = False
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            value = attrs["id"]
            if value in self.ids:
                self.errors.append(f"duplicate id: {value}")
            self.ids.add(value)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "title":
            self.has_title = True
        if tag == "meta":
            if attrs.get("name") == "description" and attrs.get("content", "").strip():
                self.has_description = True
            if attrs.get("name") == "viewport":
                self.has_viewport = True
        if tag == "img" and "alt" not in attrs:
            self.errors.append("image is missing alt")
        if tag == "a" and not attrs.get("href", "").strip():
            self.errors.append("anchor is missing a usable href")
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")


def output_path(root, path):
    candidate = (root / unquote(path).lstrip("/")).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError("reference escapes output directory")
    if candidate.is_dir() or path.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def check_reference(root, source_route, reference, documents):
    url = urlsplit(urljoin(ORIGIN + source_route, reference))
    if url.scheme not in ("http", "https"):
        return f"unsupported link scheme: {reference}"
    if url.netloc != urlsplit(ORIGIN).netloc:
        return None
    try:
        target = output_path(root, url.path)
    except ValueError as error:
        return str(error)
    if not target.is_file():
        return f"missing target: {reference}"
    fragment = unquote(url.fragment)
    if fragment and target.suffix == ".html":
        doc = documents.get(target)
        if doc is None:
            doc = Document(target.read_text(encoding="utf-8"))
        if fragment not in doc.ids:
            return f"missing fragment: {reference}"
    return None


def check_assets(root):
    errors = []
    for name, (expected_hash, dimensions) in ASSETS.items():
        path = root / "assets" / name
        if not path.is_file():
            errors.append(f"missing logo: {name}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_hash:
            errors.append(f"logo bytes changed: {name}")
        if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24 or struct.unpack(">II", data[16:24]) != dimensions:
            errors.append(f"logo dimensions changed: {name}")
    return errors


def check_metadata(doc, route):
    errors = list(doc.errors)
    locale = "ja" if route.startswith("/ja/") else "en"
    if doc.lang != locale:
        errors.append(f"expected html lang={locale}")
    if doc.h1_count != 1 or doc.main_count != 1:
        errors.append("expected exactly one h1 and one main")
    if not all((doc.has_title, doc.has_description, doc.has_viewport)):
        errors.append("missing page metadata")
    if doc.canonical != [ORIGIN + route]:
        errors.append("incorrect canonical URL")
    if route != "/404.html":
        english_route = route[3:] if locale == "ja" else route
        expected = {"en": ORIGIN + english_route, "ja": ORIGIN + "/ja" + english_route, "x-default": ORIGIN + english_route}
        if doc.alternates != expected:
            errors.append("incorrect language alternates")
    return errors


def check_external(urls):
    errors = []
    for url in sorted(urls):
        try:
            request = Request(url, headers={"User-Agent": "Project-KISS-link-check/0.1"}, method="HEAD")
            try:
                with urlopen(request, timeout=12) as response:
                    status = response.status
            except HTTPError as error:
                if error.code != 405:
                    raise
                with urlopen(Request(url, headers={"User-Agent": "Project-KISS-link-check/0.1"}), timeout=12) as response:
                    status = response.status
            if status >= 400:
                errors.append(f"external HTTP {status}: {url}")
            else:
                print(f"external {status}: {url}")
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            errors.append(f"external unresolved: {url} ({type(error).__name__})")
    return errors


def check_site(root, external=False):
    root = root.resolve()
    documents = {p.resolve(): Document(p.read_text(encoding="utf-8")) for p in sorted(root.rglob("*.html"))}
    errors = []
    external_urls = set()
    references = 0
    expected_routes = {"/" + prefix + route for prefix in ("", "ja/") for route in ROUTES} | {"/404.html"}
    actual_routes = set()
    for path, doc in documents.items():
        route = "/" + path.relative_to(root).as_posix()
        if route.endswith("index.html"):
            route = route[:-len("index.html")]
        actual_routes.add(route)
        for error in check_metadata(doc, route):
            errors.append(f"{route}: {error}")
        for reference in doc.references:
            references += 1
            error = check_reference(root, route, reference, documents)
            if error:
                errors.append(f"{route}: {error}")
            url = urlsplit(urljoin(ORIGIN + route, reference))
            if url.scheme in ("http", "https") and url.netloc != urlsplit(ORIGIN).netloc:
                external_urls.add(url._replace(fragment="").geturl())
    if expected_routes != actual_routes:
        errors.append(f"route mismatch: missing={sorted(expected_routes-actual_routes)}, extra={sorted(actual_routes-expected_routes)}")
    errors.extend(check_assets(root))
    for name, expected in (("CNAME", "kiss.i-pp.co.jp"), (".nojekyll", "")):
        path = root / name
        if not path.is_file() or path.read_text().strip() != expected:
            errors.append(f"incorrect or missing {name}")
    try:
        tree = ET.parse(root / "sitemap.xml")
        locations = [element.text for element in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        if set(locations) != {ORIGIN + route for route in expected_routes - {"/404.html"}} or len(locations) != 14:
            errors.append("sitemap does not match the language pairs")
    except (OSError, ET.ParseError):
        errors.append("missing or invalid sitemap")
    robots = root / "robots.txt"
    if not robots.is_file() or f"Sitemap: {ORIGIN}/sitemap.xml" not in robots.read_text():
        errors.append("missing sitemap in robots.txt")
    if external:
        errors.extend(check_external(external_urls))
    return errors, len(documents), references, len(external_urls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("dist"))
    parser.add_argument("--external", action="store_true", help="also perform bounded live checks on external links")
    args = parser.parse_args()
    errors, pages, references, externals = check_site(args.root, args.external)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{'FAIL' if errors else 'PASS'}: {pages} pages; {references} references; 7 language pairs; 2 original logo hashes; {externals} external URLs {'checked live' if args.external else 'not fetched'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
