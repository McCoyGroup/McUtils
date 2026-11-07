import os, tempfile, unittest
from McUtils.Extensions import platform_tag, platform_library_candidates, resolve_platform_library
from McUtils.Extensions.SharedLibraryManager import SharedLibraryLoader


class PlatformLibraryTests(unittest.TestCase):

    def test_tag_shape_and_override(self):
        tag = platform_tag()
        self.assertIn('-', tag)
        os.environ['MCUTILS_PLATFORM_TAG'] = 'linux-aarch64'
        try:
            self.assertEqual(platform_tag(), 'linux-aarch64')
        finally:
            del os.environ['MCUTILS_PLATFORM_TAG']

    def test_candidates(self):
        self.assertEqual(
            platform_library_candidates('/x/libfoo.so', tag='linux-aarch64'),
            ['/x/libfoo.linux-aarch64.so', '/x/libfoo.so']
        )
        self.assertEqual(
            platform_library_candidates('/x/libfoo.so', tag='darwin-arm64'),
            ['/x/libfoo.darwin-arm64.so', '/x/libfoo.darwin-arm64.dylib', '/x/libfoo.so']
        )

    def test_resolution_prefers_tagged_and_falls_back(self):
        with tempfile.TemporaryDirectory() as d:
            plain = os.path.join(d, 'libfoo.so')
            self.assertEqual(resolve_platform_library(plain), plain)  # nothing exists
            open(plain, 'w').close()
            self.assertEqual(resolve_platform_library(plain, tag='linux-x86_64'), plain)
            tagged = os.path.join(d, 'libfoo.linux-x86_64.so')
            open(tagged, 'w').close()
            self.assertEqual(resolve_platform_library(plain, tag='linux-x86_64'), tagged)
            self.assertEqual(resolve_platform_library(plain, tag='darwin-arm64'), plain)

    def test_loader_uses_tagged_file(self):
        with tempfile.TemporaryDirectory() as d:
            plain = os.path.join(d, 'libfoo.so')
            tagged = os.path.join(d, 'libfoo.' + platform_tag() + '.so')
            open(plain, 'w').close(); open(tagged, 'w').close()
            self.assertEqual(SharedLibraryLoader(plain)._lib_file, tagged)
