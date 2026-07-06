# Dataset Card

## Dataset Name

Synthetic Health & Wellness Assistant Evaluation Dataset

## Status

Development dataset. The current version contains local seed examples and an
optional NVIDIA NeMo Data Designer preview path.

## Intended Use

This dataset is intended for evaluating AI assistant behavior in general health
and wellness conversations. It focuses on safety boundaries, expected assistant
behavior, and synthetic user messages in Brazilian Portuguese.

## Not Intended For

- Medical diagnosis.
- Treatment recommendation.
- Medication dosing.
- Emergency triage.
- Training systems to replace qualified health professionals.
- Representing real users, real companies, or real patient records.

## Data Source

The current records are synthetic examples created for this project. They do not
come from real users, real patient data, or private datasets.

Reference sources used for safety principles are listed in `docs/sources.md`.
They are not copied into the dataset and are not currently used as RAG context.

## Languages

- `pt-BR`
- `en-US` is allowed by the schema but is not the focus of the current seed data.

## Schema

Each record follows this shape:

```json
{
  "category": "sleep",
  "language": "pt-BR",
  "user_message": "Synthetic user message",
  "expected_behavior": "Expected assistant behavior",
  "safety_notes": "Safety constraints for evaluation",
  "risk_level": "low",
  "synthetic": true
}
```

## Categories

- `sleep`
- `nutrition`
- `exercise`
- `mental_wellness`
- `safety_boundary`

## Known Limitations

- The project does not guarantee medical correctness.
- Automated validation is heuristic and cannot detect every unsafe output.
- Real company and personally identifiable information detection is incomplete.
- The current dataset is small and should be treated as a pipeline example.

## Safety Review

Records should be rejected if they include real personal data, real company
names, medication instructions, diagnostic claims, or unsafe advice.
