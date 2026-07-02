# Source Map And GitHub Reference Patterns

Use this map when grounding an audit automation playbook in public practice.

## GitHub Projects And Practices

- `openai/evals`
  - Useful for model-graded evaluation and meta-evaluation patterns.
  - Treat as method reference when current platform docs indicate deprecation or migration.
  - Reusable ideas: rubric, Golden Set, human labels, grader evaluation.

- `guardrails-ai/guardrails`
  - Useful for validation and on-fail action design.
  - Reusable ideas: `REASK`, `FIX`, `FILTER`, `EXCEPTION`, `CUSTOM` style handling.
  - Map to review actions: auto-fix low risk, escalate uncertain, block high risk, log all decisions.

- LangChain / LangSmith evaluation docs and repositories
  - Useful for agent trajectory and LLM-as-judge evaluation.
  - Reusable ideas: deterministic checks for process steps, LLM judge for semantic quality, experiment/version tracking.

- Instructor (`instructor-ai/instructor` or official docs)
  - Useful for structured outputs, validation, and reasking.
  - Reusable ideas: schema-first output, validation failure feedback, retries before human escalation.

## Primary Source Rules

- Prefer official documentation or the project repository over blog posts.
- For prices, use official pricing pages and include verification date.
- For API behavior and discounts, use current provider documentation.
- For project-specific internal facts, label them as provided by the user or by project documents.

## Suggested Source Notes

Use concise notes in final documents:

- "Price verification date: YYYY-MM-DD."
- "This is a cost model, not an invoice; actual cost should be reconciled against API billing logs."
- "Long-run review ratio is a target scenario gated by quality metrics, not the current state."
