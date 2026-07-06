"""Human-readable review reports for generated datasets."""

from pathlib import Path

from synthetic_health_eval.schema import EvaluationExample


def write_dataset_review_markdown(examples: list[EvaluationExample], output_path: Path) -> None:
    """Write a Markdown report for human review of generated examples."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Dataset Review",
        "",
        f"Total records: {len(examples)}",
        "",
        "## Summary",
        "",
        "| # | Category | Risk | Language | User message preview |",
        "|---|---|---|---|---|",
    ]

    for index, example in enumerate(examples, start=1):
        preview = _compact(example.user_message)
        lines.append(
            f"| {index} | {example.category} | {example.risk_level} | {example.language} | {preview} |"
        )

    lines.extend(["", "## Records", ""])

    for index, example in enumerate(examples, start=1):
        lines.extend(
            [
                f"### Record {index}",
                "",
                f"- Category: `{example.category}`",
                f"- Risk: `{example.risk_level}`",
                f"- Language: `{example.language}`",
                f"- Synthetic: `{example.synthetic}`",
                "",
                "**User Message**",
                "",
                example.user_message,
                "",
                "**Expected Behavior**",
                "",
                example.expected_behavior,
                "",
                "**Safety Notes**",
                "",
                example.safety_notes,
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def _compact(value: str, max_length: int = 90) -> str:
    compacted = " ".join(value.split()).replace("|", "\\|")
    if len(compacted) <= max_length:
        return compacted
    return f"{compacted[: max_length - 3]}..."
