"""Tests for the optional NeMo Data Designer pipeline configuration."""

import unittest

from synthetic_health_eval.nemo_pipeline import build_data_designer_config


class NemoPipelineConfigTest(unittest.TestCase):
    def test_builds_data_designer_config(self) -> None:
        config_builder = build_data_designer_config()
        config = config_builder.build()

        column_names = [column.name for column in config.columns]

        self.assertIn("category", column_names)
        self.assertIn("example", column_names)


if __name__ == "__main__":
    unittest.main()
