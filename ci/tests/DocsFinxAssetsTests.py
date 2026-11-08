"""Where single-file pages get the finx styles from: the vendored copy (default, no network), CDN links, a fetch
with a vendored fallback, or a local finx checkout."""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import os
import tempfile
import unittest
import urllib.request
import warnings
from unittest import mock

from McUtils.Docs import static_markdown
from McUtils.Docs import HTMLDocs


def _no_network(*args, **kwargs):
    raise AssertionError("the network was used")


def _offline(*args, **kwargs):
    raise OSError("[Errno -3] Temporary failure in name resolution")


class _Response:
    def __init__(self, text):
        self.text = text

    def read(self):
        return self.text.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FinxAssetTests(unittest.TestCase):
    def setUp(self):
        HTMLDocs._FINX_ASSET_CACHE.clear()
        self.addCleanup(HTMLDocs._FINX_ASSET_CACHE.clear)
        with open(os.path.join(HTMLDocs._FINX_VENDORED, "css", "style.css"), encoding="utf-8") as f:
            self.style_css = f.read()

    def test_vendored_files_are_packaged(self):
        for kind, names in (("css", HTMLDocs._FINX_CSS_FILES), ("js", HTMLDocs._FINX_JS_FILES)):
            for name in names:
                path = os.path.join(HTMLDocs._FINX_VENDORED, kind, name)
                self.assertTrue(os.path.isfile(path), path)
                self.assertGreater(os.path.getsize(path), 0, path)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_default_is_vendored_and_needs_no_network(self):
        with mock.patch.object(urllib.request, "urlopen", _no_network):
            html = static_markdown("# Heading\n\ntext\n", title="Offline")
        self.assertIn(self.style_css.strip()[:200], html)
        self.assertNotIn("cdn.jsdelivr.net", html)
        self.assertNotIn("raw.githubusercontent.com", html)

    def test_vendored_with_js(self):
        with mock.patch.object(urllib.request, "urlopen", _no_network):
            elems = HTMLDocs._bake_finx_assets(include_js=True)
        text = "".join(e.tostring() for e in elems)
        self.assertIn("finxJS", text)                          # init.js inlined
        self.assertIn(HTMLDocs._JQUERY_URL, text)              # jQuery stays a browser-side script

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_link_mode_points_the_browser_at_a_pinned_copy(self):
        with mock.patch.object(urllib.request, "urlopen", _no_network):
            html = static_markdown("text", finx_assets="link")
        base = HTMLDocs._FINX_CDN.format(ref=HTMLDocs.FINX_VENDORED_REF)
        for name in HTMLDocs._FINX_CSS_FILES:
            self.assertIn(f'href="{base}/css/{name}"', html)
        self.assertNotIn(self.style_css.strip()[:200], html)
        with mock.patch.object(urllib.request, "urlopen", _no_network):
            elems = HTMLDocs._bake_finx_assets(include_js=True, assets="link", extra_css=".x{color:red}")
        text = "".join(e.tostring() for e in elems)
        self.assertIn(f'src="{base}/js/init.js"', text)
        self.assertIn(".x{color:red}", text)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_fetch_mode_uses_the_download(self):
        with mock.patch.object(urllib.request, "urlopen", lambda url, timeout=None: _Response(f"/* from {url} */")):
            html = static_markdown("text", finx_assets="fetch")
        self.assertIn("/* from https://raw.githubusercontent.com/McCoyGroup/finx/master/assets/css/style.css */", html)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_fetch_mode_falls_back_to_vendored_when_offline(self):
        with mock.patch.object(urllib.request, "urlopen", _offline), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            html = static_markdown("text", finx_assets="fetch")
        self.assertIn(self.style_css.strip()[:200], html)
        self.assertTrue(any("vendored" in str(w.message) and issubclass(w.category, RuntimeWarning) for w in caught),
                        [str(w.message) for w in caught])

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_local_checkout_directory(self):
        with tempfile.TemporaryDirectory() as root:
            for kind, names in (("css", HTMLDocs._FINX_CSS_FILES), ("js", HTMLDocs._FINX_JS_FILES)):
                os.makedirs(os.path.join(root, "assets", kind))
                for name in names:
                    with open(os.path.join(root, "assets", kind, name), "w") as f:
                        f.write(f"/* local {name} */")
            with mock.patch.object(urllib.request, "urlopen", _no_network):
                for d in (root, os.path.join(root, "assets")):       # the checkout or its assets directory
                    html = static_markdown("text", finx_assets=d)
                    self.assertIn("/* local style.css */", html)
                    self.assertIn("/* local pygment_trac.css */", html)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_missing_file_in_directory(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(FileNotFoundError):
                static_markdown("text", finx_assets=root)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_bad_mode(self):
        for bad in ("remote", 3, "/no/such/finx/dir"):
            with self.assertRaises(ValueError):
                static_markdown("text", finx_assets=bad)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_module_default_can_be_changed(self):
        old = HTMLDocs.default_finx_assets
        self.addCleanup(setattr, HTMLDocs, "default_finx_assets", old)
        HTMLDocs.default_finx_assets = "link"
        with mock.patch.object(urllib.request, "urlopen", _no_network):
            html = static_markdown("text")
        self.assertIn("cdn.jsdelivr.net/gh/McCoyGroup/finx@", html)


if __name__ == "__main__":
    unittest.main()
