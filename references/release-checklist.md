# Release Checklist For Audit Automation Playbooks

Use this checklist before delivering a release-ready document.

## Scientific And Business Validity

- Separate actuals, estimates, and targets.
- Define the manual baseline before showing automation savings.
- Show formulas or enough assumptions to reproduce cost numbers.
- Include both personnel cost and model/API cost.
- Mark the current state honestly: shadow mode, assisted mode, supervised mode, or fully launched.
- Do not claim low human-review ratios unless gates are stated.

## Required Gates Before Reducing Human Review

Use these default gates unless the user provides stronger project-specific gates:

- Overall AI-human agreement >=95% on recent batches.
- High-risk/C-grade false negative rate <5%.
- One-vote veto false negative count = 0 in the latest critical sample, or explicitly escalated for business acceptance.
- Golden Set includes edge cases and disputed historical samples.
- Rules, prompt/model versions, and human decisions are traceable.
- At least one post-change regression run exists after each rule or prompt update.

## Cost Scenario Hygiene

Every comparison table should include:

- Pure manual baseline.
- Current state.
- Domestic/local model.
- Overseas model.
- Hybrid routing model.
- Long-run target scenario.

For each scenario, include:

- Annual personnel cost.
- Annual model cost.
- Annual total cost.
- Savings vs pure manual.
- Savings rate vs pure manual.

## Readability And Format

- Put the recommended path in the first page.
- Keep one main cost table; move detailed formulas to the cost chapter.
- Avoid half-translated table text, broken words, and raw Mermaid/code blocks unless the document renderer supports them.
- Use consistent units: orders/month, person-days/month, CNY/year, tokens/order.
- Use `～` for ranges in Chinese business documents.

## Risk Language

Prefer concrete risk language:

- "C-grade false negative rate"
- "one-vote veto leakage"
- "AI-human agreement"
- "manual review ratio"
- "rule/model version traceability"

Avoid vague claims:

- "AI is accurate"
- "fully automated" when manual import remains
- "cost nearly zero" without model and personnel cost split
