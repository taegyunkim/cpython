import textwrap
import unittest
from test.support import import_helper
from test.support import script_helper


_testcapi = import_helper.import_module("_testcapi")


class DebugMetadataTests(unittest.TestCase):
    def test_runtime_metadata(self):
        address, size, prefix = _testcapi.get_debug_metadata("PyRuntime")
        self.assertGreater(address, 0)
        self.assertGreaterEqual(size, len(prefix))
        self.assertEqual(prefix, b"xdebugpy")

    def test_unknown_metadata(self):
        self.assertIsNone(_testcapi.get_debug_metadata("missing"))

    def test_asyncio_metadata_is_registered_on_import(self):
        code = textwrap.dedent("""
            import struct
            import _testcapi

            assert _testcapi.get_debug_metadata("AsyncioDebug") is None
            import _asyncio
            address, size, prefix = _testcapi.get_debug_metadata("AsyncioDebug")
            assert address > 0
            assert size == 13 * 8
            assert struct.unpack("=Q", prefix)[0] > 0
        """)
        script_helper.assert_python_ok("-S", "-c", code)


if __name__ == "__main__":
    unittest.main()
