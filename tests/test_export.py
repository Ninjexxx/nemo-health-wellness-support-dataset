"""Tests for dataset export helpers."""

import json
import tempfile
import unittest
from pathlib import Path

from synthetic_health_eval.export import write_examples_jsonl
from synthetic_health_eval.seed_examples import build_seed_examples


class JsonlExportTest(unittest.TestCase):
    def test_writes_one_json_object_per_line(self) -> None:
        examples = build_seed_examples()[:2]

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "dataset.jsonl"
            write_examples_jsonl(examples, output_path)

            lines = output_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0])["category"], "sleep")
        self.assertEqual(json.loads(lines[1])["category"], "nutrition")


if __name__ == "__main__":
    unittest.main()
