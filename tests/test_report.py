"""Tests for Markdown review report generation."""

import tempfile
import unittest
from pathlib import Path

from synthetic_health_eval.report import write_dataset_review_markdown
from synthetic_health_eval.seed_examples import build_seed_examples


class DatasetReviewReportTest(unittest.TestCase):
    def test_writes_markdown_report(self) -> None:
        examples = build_seed_examples()[:1]

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "review.md"
            write_dataset_review_markdown(examples, output_path)
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("# Dataset Review", content)
        self.assertIn("Total records: 1", content)
        self.assertIn("## Records", content)


if __name__ == "__main__":
    unittest.main()
