# Reference Sources

This project generates synthetic data for evaluating AI assistants in health and
wellness scenarios. The sources below are not used as a live retrieval system and
are not copied into the generated dataset. They guide the safety principles,
topic boundaries, and review criteria used by the project.

## Scope

The dataset should support evaluation of general wellness assistant behavior,
not clinical decision making. Generated examples should avoid diagnosis,
medication instructions, treatment plans, emergency triage, or claims that
replace professional care.

## Sources

### Physical activity

- World Health Organization, "Physical activity":
  https://www.who.int/news-room/fact-sheets/detail/physical-activity

Relevant project guidance:

- Prefer general encouragement to move more and sit less.
- Avoid personalized exercise prescriptions for users with symptoms or medical
  conditions.
- Recommend professional guidance when pain, injury history, pregnancy, chronic
  illness, or concerning symptoms are mentioned.

### Sleep

- Centers for Disease Control and Prevention, "About Sleep":
  https://www.cdc.gov/sleep/about/index.html

Relevant project guidance:

- Prefer general sleep hygiene examples: consistent schedule, relaxing
  environment, caffeine timing, device use, exercise, and healthy routines.
- Do not provide medication dosing or sedative recommendations.
- Recommend a healthcare provider when sleep problems are regular, severe, or
  suggest a sleep disorder.

### Mental wellness

- World Health Organization, "Mental health":
  https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response

Relevant project guidance:

- Treat mental wellness as a broad continuum, not as a diagnosis.
- Prefer supportive, non-clinical coping strategies.
- Escalate to professional or emergency support when distress is intense,
  persistent, or involves risk of self-harm or harm to others.

### Nutrition

- Dietary Guidelines for Americans:
  https://www.dietaryguidelines.gov/

Relevant project guidance:

- Prefer general food planning, routine, balance, and accessibility.
- Avoid individualized diet prescriptions, calorie targets, supplement advice,
  or weight-loss promises.
- Recommend qualified professionals for medical conditions, eating disorders,
  pregnancy, allergies, or complex dietary needs.

## Not RAG

This project does not currently implement retrieval-augmented generation. These
sources are documented references for humans and for project rules. A future RAG
version would retrieve relevant passages at generation time and pass them to the
model as context.

## Review Rule

If generated content conflicts with the safety principles above, the generated
example should be rejected or rewritten before export.
