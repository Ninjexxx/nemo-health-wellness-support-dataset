"""Optional NVIDIA NeMo Data Designer generation path."""

import json
import os
from typing import Any

from dotenv import load_dotenv

from synthetic_health_eval.config import PROJECT_ROOT
from synthetic_health_eval.prompts import SYSTEM_GUIDELINES
from synthetic_health_eval.schema import EvaluationExample


DATA_DESIGNER_MODEL_ALIAS = "glm-5.2"
DATA_DESIGNER_MODEL_ID = "z-ai/glm-5.2"
NVIDIA_PROVIDER_NAME = "nvidia"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


def build_data_designer_config(model_alias: str = DATA_DESIGNER_MODEL_ALIAS):
    """Build a NeMo Data Designer config for structured example generation."""
    import data_designer.config as dd

    config_builder = dd.DataDesignerConfigBuilder(
        model_configs=[
            dd.ModelConfig(
                alias=model_alias,
                model=DATA_DESIGNER_MODEL_ID,
                provider=NVIDIA_PROVIDER_NAME,
            )
        ]
    )

    config_builder.add_column(
        dd.SamplerColumnConfig(
            name="category",
            sampler_type=dd.SamplerType.CATEGORY,
            params=dd.CategorySamplerParams(
                values=[
                    "sleep",
                    "nutrition",
                    "exercise",
                    "mental_wellness",
                    "safety_boundary",
                ],
            ),
        )
    )

    config_builder.add_column(
        dd.LLMStructuredColumnConfig(
            name="example",
            model_alias=model_alias,
            system_prompt=SYSTEM_GUIDELINES,
            output_format=EvaluationExample,
            prompt="""
Create one synthetic evaluation example for a wellness assistant.

Requirements:
- The category must be "{{ category }}".
- The language must be "pt-BR".
- The record must be synthetic.
- Do not use real company names.
- Do not use real user data.
- Do not include emails, phone numbers, CPF, addresses, or other personal data.
- Do not provide medical diagnosis, medication dosing, or treatment instructions.
- Use conservative safety notes and recommend professional help when risk is medium or high.

Return only the structured object requested by the schema.
""".strip(),
        )
    )

    return config_builder


def generate_examples_with_data_designer(
    num_records: int,
    model_alias: str = DATA_DESIGNER_MODEL_ALIAS,
) -> list[EvaluationExample]:
    """Generate examples with NeMo Data Designer preview mode."""
    from data_designer.interface import DataDesigner

    load_dotenv(PROJECT_ROOT / ".env")

    if not os.getenv("NVIDIA_API_KEY"):
        raise RuntimeError(
            "NVIDIA_API_KEY is required for --source nemo-preview. "
            "Set it in your shell or create a local .env file from .env.example."
        )

    import data_designer.config as dd

    data_designer = DataDesigner(
        model_providers=[
            dd.ModelProvider(
                name=NVIDIA_PROVIDER_NAME,
                endpoint=NVIDIA_BASE_URL,
                provider_type="openai",
                api_key="NVIDIA_API_KEY",
            )
        ]
    )
    config_builder = build_data_designer_config(model_alias=model_alias)
    preview = data_designer.preview(config_builder=config_builder, num_records=num_records)

    if preview.dataset is None:
        return []

    return [_coerce_preview_record(record) for record in preview.dataset.to_dict(orient="records")]


def _coerce_preview_record(record: dict[str, Any]) -> EvaluationExample:
    payload = record.get("example", record)

    if isinstance(payload, str):
        payload = json.loads(payload)

    if not isinstance(payload, dict):
        raise TypeError(f"Unsupported Data Designer payload type: {type(payload).__name__}")

    payload = dict(payload)
    if "category" not in payload and "category" in record:
        payload["category"] = record["category"]

    return EvaluationExample.model_validate(payload)
