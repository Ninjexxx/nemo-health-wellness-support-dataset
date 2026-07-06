"""Export helpers for synthetic evaluation datasets."""

import json
from collections.abc import Iterable
from pathlib import Path

from synthetic_health_eval.schema import EvaluationExample


def write_examples_jsonl(
    examples: Iterable[EvaluationExample],
    output_path: Path,
) -> None:
    """Write validated evaluation examples to a JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for example in examples:
            record = example.model_dump()
            file.write(json.dumps(record, ensure_ascii=False))
            file.write("\n")
