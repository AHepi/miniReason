"""Windows long-path regressions for the immutable blob store.

Vendored from AHepi/DeepReason@9607fba tests/test_blob_store_long_paths.py;
see VENDOR_NOTES.md.
"""

from __future__ import annotations

import os
import unittest.mock
from pathlib import Path

from deepreason_core.canonical import sha256_hex
from deepreason_core.storage.blobs import BlobStore, _io_path

from .helpers import TempDirTestCase


def _long_blob_root(tmp_path: Path) -> Path:
    segments = [f"blob-long-segment-{index}-" + ("x" * 72) for index in range(4)]
    return tmp_path.joinpath(*segments, "blobs")


class BlobStoreLongPathTests(TempDirTestCase):
    def test_long_path_atomic_temp_write_final_read_and_exists(self) -> None:
        root = _long_blob_root(self.tmp_path)
        data = b"canonical blob bytes remain independent of the filesystem path"
        replacements: list[tuple[Path, Path, bytes]] = []
        real_replace = os.replace

        def observe_replace(source, target) -> None:
            source_path = Path(source)
            target_path = Path(target)
            self.assertTrue(source_path.exists())
            self.assertEqual(source_path.read_bytes(), data)
            self.assertFalse(target_path.exists())
            replacements.append((source_path, target_path, source_path.read_bytes()))
            real_replace(source, target)

        with unittest.mock.patch.object(os, "replace", observe_replace):
            store = BlobStore(root)
            ref = store.put(data)
            logical_path = store._path(ref)

            self.assertEqual(ref, sha256_hex(data))
            self.assertEqual(logical_path, root / ref[:2] / ref)
            self.assertGreater(len(os.path.abspath(str(logical_path))), 260)
            self.assertTrue(replacements)
            temp_path, final_path, written = replacements[0]
            self.assertEqual(temp_path.name, f"{ref}.tmp.{os.getpid()}")
            self.assertEqual(final_path.name, ref)
            self.assertEqual(written, data)
            if os.name == "nt":
                self.assertTrue(str(temp_path).startswith("\\\\?\\"))
                self.assertTrue(str(final_path).startswith("\\\\?\\"))

            self.assertEqual(store.get(ref), data)
            self.assertEqual(store.resolve_prefix(ref[:12]), ref)

            # A second put exercises the long final-path existence check and
            # does not create or replace another temporary file.
            self.assertEqual(store.put(data), ref)
            self.assertEqual(len(replacements), 1)
            self.assertTrue(
                all(".tmp." not in item.name for item in final_path.parent.iterdir())
            )

    def test_long_path_read_only_store_reads_without_creating_or_writing(self) -> None:
        root = _long_blob_root(self.tmp_path)
        data = b"read-only long-path blob"
        writable = BlobStore(root)
        ref = writable.put(data)

        read_only = BlobStore(root, read_only=True)
        self.assertEqual(read_only.root, root)
        self.assertEqual(read_only.get(ref), data)
        self.assertEqual(read_only.resolve_prefix(ref[:16]), ref)
        with self.assertRaisesRegex(RuntimeError, "read-only"):
            read_only.put(b"must not be written")

        missing_root = root / ("missing-read-only-" + ("y" * 80))
        self.assertFalse(_io_path(missing_root).exists())
        BlobStore(missing_root, read_only=True)
        self.assertFalse(_io_path(missing_root).exists())
