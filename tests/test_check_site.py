"""Failure cases protecting navigation, localization, and unchanged brand assets."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_site import Document, ORIGIN, check_assets, check_metadata, check_reference, output_path


class SiteChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "docs" / "index.html"
        self.target.parent.mkdir()
        self.target.write_text('<h2 id="日本語">Example</h2>')
        self.documents = {self.target: Document(self.target.read_text())}

    def test_valid_relative_and_encoded_fragment(self):
        self.assertIsNone(check_reference(self.root, "/products/", "../docs/#%E6%97%A5%E6%9C%AC%E8%AA%9E", self.documents))

    def test_missing_page_is_rejected(self):
        self.assertIn("missing target", check_reference(self.root, "/", "/missing/", self.documents))

    def test_missing_fragment_is_rejected(self):
        self.assertIn("missing fragment", check_reference(self.root, "/", "/docs/#unknown", self.documents))

    def test_unsafe_link_scheme_is_rejected(self):
        self.assertIn("unsupported", check_reference(self.root, "/", "javascript:alert(1)", self.documents))

    def test_encoded_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            output_path(self.root, "/%2e%2e/escape")

    def test_duplicate_ids_and_missing_image_alt_are_rejected(self):
        document = Document('<h1 id="x">Title</h1><p id="x">Text</p><img src="logo.png">')
        self.assertIn("duplicate id: x", document.errors)
        self.assertIn("image is missing alt", document.errors)

    def test_incorrect_language_pair_is_rejected(self):
        document = Document(f'<html lang="ja"><title>Title</title><meta name="description" content="Description"><meta name="viewport" content="width=device-width"><link rel="canonical" href="{ORIGIN}/ja/docs/"><main><h1>Title</h1></main></html>')
        self.assertEqual(check_metadata(document, "/ja/docs/"), ["incorrect language alternates"])

    def test_empty_document_fails_metadata(self):
        self.assertGreaterEqual(len(check_metadata(Document(""), "/")), 4)

    def test_modified_logo_is_rejected(self):
        directory = self.root / "assets"
        directory.mkdir()
        (directory / "project-kiss.png").write_bytes(b"not the original logo")
        self.assertIn("logo bytes changed: project-kiss.png", check_assets(self.root))
        self.assertIn("missing logo: project-aceis.png", check_assets(self.root))

    def test_external_reference_is_not_treated_as_a_local_file(self):
        self.assertIsNone(check_reference(self.root, "/", "https://github.com/i-pp", self.documents))


if __name__ == "__main__":
    unittest.main()
