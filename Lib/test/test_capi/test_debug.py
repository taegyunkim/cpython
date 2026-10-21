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
            assert size == 16 * 8
            assert prefix == b"xasyncpy"
        """)
        script_helper.assert_python_ok("-S", "-c", code)

    def test_asyncio_debug_offsets_reachable_from_runtime(self):
        import_helper.import_module("ctypes")
        code = textwrap.dedent("""
            import ctypes
            import struct
            import sys
            import _testcapi

            runtime = ctypes.addressof(
                ctypes.c_char.in_dll(ctypes.pythonapi, "_PyRuntime"))
            # _Py_DebugOffsets: cookie, version, free_threaded, then
            # runtime_state: size, finalizing, interpreters_head,
            # asyncio_debug_offsets.
            cookie, version, _ = struct.unpack(
                "=8sQQ", ctypes.string_at(runtime, 24))
            assert cookie == b"xdebugpy"
            assert version == sys.hexversion
            pointer_offset = struct.unpack(
                "=Q", ctypes.string_at(runtime + 48, 8))[0]

            def asyncio_table():
                return ctypes.c_void_p.from_address(
                    runtime + pointer_offset).value

            assert asyncio_table() is None
            import _asyncio
            address = asyncio_table()
            assert address == _testcapi.get_debug_metadata("AsyncioDebug")[0]
            cookie, table_version, size = struct.unpack(
                "=8sQQ", ctypes.string_at(address, 24))
            assert cookie == b"xasyncpy"
            assert table_version == version
            assert size == 16 * 8
        """)
        script_helper.assert_python_ok("-S", "-c", code)


if __name__ == "__main__":
    unittest.main()
