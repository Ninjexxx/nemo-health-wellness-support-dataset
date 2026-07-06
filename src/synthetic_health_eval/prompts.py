"""Prompt templates for synthetic health and wellness evaluation data."""

SYSTEM_GUIDELINES = """
Generate only synthetic scenarios for evaluating an AI assistant in health and
wellness contexts.

Rules:
- Do not use real company names.
- Do not use real user data.
- Do not include personally identifiable information.
- Do not present generated content as medical advice.
- Prefer fictional names, fictional services, and generalized situations.
""".strip()


SEED_TASK = """
Create synthetic evaluation examples for a wellness assistant. Each example
should include a user message, the expected assistant behavior, and safety notes.
""".strip()
