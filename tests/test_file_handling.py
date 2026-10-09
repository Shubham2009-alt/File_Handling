"""Unit tests for the file_handling module."""

import tempfile
import unittest
from pathlib import Path

from file_handling import (
    append_to_file,
    create_file,
    delete_file,
    overwrite_file,
    read_file,
    rename_file,
)


class FileHandlingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def test_create_file(self) -> None:
        path = self.root / "notes.txt"
        result = create_file(path)
        self.assertEqual(result, path)
        self.assertTrue(path.is_file())
        self.assertEqual(path.read_text(encoding="utf-8"), "")

    def test_create_does_not_overwrite_existing_file(self) -> None:
        path = self.root / "notes.txt"
        path.write_text("keep this", encoding="utf-8")

        with self.assertRaises(FileExistsError):
            create_file(path)

        self.assertEqual(path.read_text(encoding="utf-8"), "keep this")

    def test_read_file_supports_utf8(self) -> None:
        path = self.root / "notes.txt"
        path.write_text("Hello, नमस्ते!", encoding="utf-8")
        self.assertEqual(read_file(path), "Hello, नमस्ते!")

    def test_read_missing_file_raises_error(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_file(self.root / "missing.txt")

    def test_rename_file(self) -> None:
        source = self.root / "old.txt"
        destination = self.root / "new.txt"
        source.write_text("data", encoding="utf-8")

        result = rename_file(source, destination)

        self.assertEqual(result, destination)
        self.assertFalse(source.exists())
        self.assertEqual(destination.read_text(encoding="utf-8"), "data")

    def test_rename_does_not_replace_destination(self) -> None:
        source = self.root / "old.txt"
        destination = self.root / "new.txt"
        source.write_text("source", encoding="utf-8")
        destination.write_text("destination", encoding="utf-8")

        with self.assertRaises(FileExistsError):
            rename_file(source, destination)

        self.assertEqual(source.read_text(encoding="utf-8"), "source")
        self.assertEqual(destination.read_text(encoding="utf-8"), "destination")

    def test_append_to_file(self) -> None:
        path = self.root / "notes.txt"
        path.write_text("first", encoding="utf-8")

        append_to_file(path, " second")

        self.assertEqual(path.read_text(encoding="utf-8"), "first second")

    def test_append_missing_file_does_not_create_it(self) -> None:
        path = self.root / "missing.txt"

        with self.assertRaises(FileNotFoundError):
            append_to_file(path, "text")

        self.assertFalse(path.exists())

    def test_overwrite_file(self) -> None:
        path = self.root / "notes.txt"
        path.write_text("old contents", encoding="utf-8")

        overwrite_file(path, "new contents")

        self.assertEqual(path.read_text(encoding="utf-8"), "new contents")

    def test_overwrite_missing_file_does_not_create_it(self) -> None:
        path = self.root / "missing.txt"

        with self.assertRaises(FileNotFoundError):
            overwrite_file(path, "text")

        self.assertFalse(path.exists())

    def test_delete_file(self) -> None:
        path = self.root / "notes.txt"
        path.write_text("temporary", encoding="utf-8")

        delete_file(path)

        self.assertFalse(path.exists())

    def test_delete_missing_file_raises_error(self) -> None:
        with self.assertRaises(FileNotFoundError):
            delete_file(self.root / "missing.txt")

    def test_directory_is_not_treated_as_a_file(self) -> None:
        directory = self.root / "folder"
        directory.mkdir()

        with self.assertRaises(IsADirectoryError):
            read_file(directory)

        with self.assertRaises(IsADirectoryError):
            delete_file(directory)


if __name__ == "__main__":
    unittest.main()
