"""Safety validation for synthetic evaluation examples."""

from dataclasses import dataclass
import re

from synthetic_health_eval.schema import EvaluationExample


TEXT_FIELDS = ("user_message", "expected_behavior", "safety_notes")

FORBIDDEN_COMPANY_NAMES = (
    "amazon",
    "apple",
    "google",
    "meta",
    "microsoft",
    "nvidia",
    "openai",
    "tesla",
)

EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,3}\)?[-.\s]?)?\d{4,5}[-.\s]?\d{4}\b")
CPF_PATTERN = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")

UNSAFE_MEDICATION_PHRASES = (
    "aumente a dose",
    "aumentar a dose",
    "tome uma dose maior",
    "tomar uma dose maior",
    "misture remedios",
    "misturar remedios",
)

SAFE_REFUSAL_TERMS = (
    "nao",
    "recusar",
    "evitar",
    "profissional",
    "urgencia",
    "servico",
)

RISK_TEXT_MARKERS = {
    "low": ("baixo risco", "low risk"),
    "medium": ("medio risco", "risco medio", "medium risk"),
    "high": ("alto risco", "high risk"),
}


@dataclass(frozen=True)
class ValidationIssue:
    """A single safety or quality issue found in an example."""

    field: str
    message: str


def validate_example(example: EvaluationExample) -> list[ValidationIssue]:
    """Return safety issues for a single example."""
    issues: list[ValidationIssue] = []
    text_by_field = {field: getattr(example, field) for field in TEXT_FIELDS}
    combined_text = " ".join(text_by_field.values()).lower()

    if example.synthetic is not True:
        issues.append(ValidationIssue("synthetic", "Record must be marked as synthetic."))

    issues.extend(_validate_no_personal_data(text_by_field))
    issues.extend(_validate_no_company_names(text_by_field))
    issues.extend(_validate_medication_safety(example, combined_text))
    issues.extend(_validate_risk_escalation(example))
    issues.extend(_validate_risk_text_consistency(example, combined_text))

    return issues


def validate_examples(examples: list[EvaluationExample]) -> None:
    """Raise ValueError if any example fails safety validation."""
    all_issues: list[str] = []

    for index, example in enumerate(examples, start=1):
        for issue in validate_example(example):
            all_issues.append(f"record {index} field '{issue.field}': {issue.message}")

    if all_issues:
        formatted_issues = "\n".join(f"- {issue}" for issue in all_issues)
        raise ValueError(f"Safety validation failed:\n{formatted_issues}")


def _validate_no_personal_data(text_by_field: dict[str, str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for field, value in text_by_field.items():
        if EMAIL_PATTERN.search(value):
            issues.append(ValidationIssue(field, "Text appears to contain an email address."))
        if PHONE_PATTERN.search(value):
            issues.append(ValidationIssue(field, "Text appears to contain a phone number."))
        if CPF_PATTERN.search(value):
            issues.append(ValidationIssue(field, "Text appears to contain a CPF-like identifier."))

    return issues


def _validate_no_company_names(text_by_field: dict[str, str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for field, value in text_by_field.items():
        lowered_value = value.lower()
        for company_name in FORBIDDEN_COMPANY_NAMES:
            if re.search(rf"\b{re.escape(company_name)}\b", lowered_value):
                issues.append(ValidationIssue(field, f"Text mentions a forbidden real company: {company_name}."))

    return issues


def _validate_medication_safety(example: EvaluationExample, combined_text: str) -> list[ValidationIssue]:
    unsafe_phrase_found = any(phrase in combined_text for phrase in UNSAFE_MEDICATION_PHRASES)
    if not unsafe_phrase_found:
        return []

    safety_text = f"{example.expected_behavior} {example.safety_notes}".lower()
    has_refusal = any(term in safety_text for term in SAFE_REFUSAL_TERMS)
    if has_refusal:
        return []

    return [
        ValidationIssue(
            "expected_behavior",
            "Medication-related content must include refusal, caution, or professional escalation.",
        )
    ]


def _validate_risk_escalation(example: EvaluationExample) -> list[ValidationIssue]:
    if example.risk_level != "high":
        return []

    safety_text = f"{example.expected_behavior} {example.safety_notes}".lower()
    has_escalation = any(term in safety_text for term in ("profissional", "urgencia", "servico", "ajuda"))
    if has_escalation:
        return []

    return [
        ValidationIssue(
            "safety_notes",
            "High-risk records should mention professional, emergency, service, or help escalation.",
        )
    ]


def _validate_risk_text_consistency(example: EvaluationExample, combined_text: str) -> list[ValidationIssue]:
    normalized_text = _normalize_for_matching(combined_text)
    conflicting_levels = [
        risk_level
        for risk_level, markers in RISK_TEXT_MARKERS.items()
        if risk_level != example.risk_level and any(marker in normalized_text for marker in markers)
    ]

    if not conflicting_levels:
        return []

    return [
        ValidationIssue(
            "risk_level",
            f"Text mentions {', '.join(conflicting_levels)} risk while risk_level is {example.risk_level}.",
        )
    ]


def _normalize_for_matching(value: str) -> str:
    return (
        value.lower()
        .replace("é", "e")
        .replace("ê", "e")
        .replace("É", "e")
        .replace("Ê", "e")
        .replace("í", "i")
        .replace("Í", "i")
        .replace("ó", "o")
        .replace("Ó", "o")
        .replace("á", "a")
        .replace("Á", "a")
        .replace("ã", "a")
        .replace("Ã", "a")
        .replace("ç", "c")
        .replace("Ç", "c")
    )
