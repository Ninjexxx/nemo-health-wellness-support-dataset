"""Validated data shapes for synthetic evaluation examples."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


Category = Literal[
    "sleep",
    "nutrition",
    "exercise",
    "mental_wellness",
    "safety_boundary",
]

RiskLevel = Literal["low", "medium", "high"]
Language = Literal["pt-BR", "en-US"]


class EvaluationExample(BaseModel):
    """One synthetic example used to evaluate an AI assistant."""

    category: Category
    language: Language = "pt-BR"
    user_message: str = Field(min_length=1)
    expected_behavior: str = Field(min_length=1)
    safety_notes: str = Field(min_length=1)
    risk_level: RiskLevel
    synthetic: Literal[True] = True

    @field_validator("user_message", "expected_behavior", "safety_notes")
    @classmethod
    def text_fields_must_not_be_blank(cls, value: str) -> str:
        """Reject strings that contain only whitespace."""
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Text fields must not be blank.")
        return cleaned_value
