"""Entry point for the synthetic dataset generation pipeline."""

import argparse
import json

from synthetic_health_eval.config import DEFAULT_OUTPUT_PATH, DEFAULT_REPORT_PATH, SYNTHETIC_DATA_DIR
from synthetic_health_eval.export import write_examples_jsonl
from synthetic_health_eval.nemo_pipeline import generate_examples_with_data_designer
from synthetic_health_eval.prompts import SEED_TASK, SYSTEM_GUIDELINES
from synthetic_health_eval.report import write_dataset_review_markdown
from synthetic_health_eval.seed_examples import build_seed_examples
from synthetic_health_eval.validation import validate_examples


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Generate a synthetic health and wellness evaluation dataset.")
    parser.add_argument(
        "--source",
        choices=("seed", "nemo-preview"),
        default="seed",
        help="Use local seed examples or NeMo Data Designer preview generation.",
    )
    parser.add_argument(
        "--num-records",
        type=int,
        default=5,
        help="Number of records to request when using NeMo Data Designer preview.",
    )
    return parser.parse_args()


def main() -> None:
    """Prepare the generation pipeline.

    By default, this command uses local seed examples so it can run without
    network access. Use --source nemo-preview to generate with NeMo Data Designer.
    """
    args = parse_args()
    SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Synthetic health and wellness evaluation dataset")
    print(f"Source: {args.source}")
    print(f"Output path: {DEFAULT_OUTPUT_PATH}")
    print("\nSystem guidelines:")
    print(SYSTEM_GUIDELINES)
    print("\nSeed task:")
    print(SEED_TASK)

    if args.source == "seed":
        examples = build_seed_examples()
    else:
        try:
            examples = generate_examples_with_data_designer(num_records=args.num_records)
        except RuntimeError as error:
            print(f"Error: {error}")
            raise SystemExit(1) from None

    validate_examples(examples)
    if not examples:
        raise ValueError("No examples were generated.")

    print("\nFirst validated example:")
    print(json.dumps(examples[0].model_dump(), ensure_ascii=False, indent=2))

    write_examples_jsonl(examples, DEFAULT_OUTPUT_PATH)
    print(f"\nSaved {len(examples)} examples to: {DEFAULT_OUTPUT_PATH}")

    write_dataset_review_markdown(examples, DEFAULT_REPORT_PATH)
    print(f"Saved review report to: {DEFAULT_REPORT_PATH}")


if __name__ == "__main__":
    main()
