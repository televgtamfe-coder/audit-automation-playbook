---
name: audit-automation-playbook
description: Create reusable AI audit, quality-review, compliance-review, content-moderation, customer-service QA, or order-review automation plans. Use when Codex needs to convert an existing manual review process into a rule + LLM + human-review workflow, produce cost/ROI comparisons across pure manual, domestic model, overseas model, and hybrid model options, define rollout gates, calibrate rubrics, or prepare a release-ready project playbook/document.
---

# Audit Automation Playbook

## Core Workflow

1. **Define the current manual baseline**
   - Capture monthly review volume, manual throughput, reviewer roles, annual cost by role, current QA criteria, exception rate, and current evidence sources.
   - Separate actuals from assumptions. Mark each number as `actual`, `estimated`, or `target`.

2. **Turn judgement into an executable standard**
   - Write 4-8 review dimensions.
   - Define one-vote veto items, cumulative deductions, final grade bands, required tags, and review actions.
   - Require traceable output fields: item/order id, reviewer/model version, score, grade, triggered tags, reason, action, timestamp.

3. **Design the workflow before choosing the model**
   - Use this default chain: data import -> preprocessing/filtering -> structured parsing -> rule/LLM judgement -> result formatting -> human review by risk tier -> logs/dashboard.
   - Prefer deterministic rules for red lines and field validation; use LLMs for semantic judgement and edge cases.

4. **Build the cost comparison early**
   - Always compare at least: pure manual, current state, domestic model, overseas model, hybrid model, and long-run low-review scenario.
   - Include personnel cost, model cost, total annual cost, savings vs manual, and savings rate.
   - Use `scripts/roi_calculator.py` when the user provides volume, token, model price, and personnel assumptions.

5. **Add calibration and rollout gates**
   - Build a Golden Set with human labels before any release claim.
   - Track overall accuracy, C-grade/high-risk false negatives, A-grade false positives, and Kappa/inter-rater reliability.
   - Do not recommend reducing human review below 3-5% unless accuracy and high-risk false negative gates are explicitly satisfied.

6. **Prepare release-ready output**
   - Lead with an executive conclusion and a single comparable data table.
   - Keep methodology and industry references after the project facts.
   - Clean work-in-progress artifacts: broken tables, half sentences, unverified prices, vague claims, and uncited model names.

## Recommended Output Structure

Use this order for project documents:

1. Executive summary and recommended path
2. Core data table with comparable cost scenarios
3. Current progress, completed milestones, and remaining blockers
4. Review standard and workflow design
5. Model strategy and cost/ROI model
6. Calibration, risk control, and rollout gates
7. Reuse checklist for future projects
8. References and price/source audit notes

## Cost Table Requirements

For every scenario, include the same columns:

- Scenario/status
- Model and workflow assumption
- Human review volume
- Annual personnel cost
- Annual model cost
- Annual total cost
- Savings vs pure manual
- Savings rate vs pure manual

Use these scenario patterns by default:

- **Pure manual baseline**: no model; full review volume.
- **Current state**: actual project progress and actual/manual import constraints.
- **Domestic model**: full initial screening by local/domestic model.
- **Overseas model**: full initial screening by overseas model.
- **Hybrid model**: domestic model for all basic cases, overseas model only for difficult/abnormal cases.
- **Long-run low-review**: human review ratio reduced to a gated target such as <=3%.

For hybrid routing, define difficult/abnormal triggers: low confidence, suspected high-risk grade, one-vote veto boundary, rule/model conflict, historically disputed tag, professional judgement uncertainty, complaint/refund/after-sales involvement.

## Source And Evidence Discipline

- Browse or otherwise verify current model prices, API batch discounts, and framework claims before using them in a release-ready artifact.
- Cite primary sources where practical: official docs or source repositories.
- State the price verification date. Prices and model availability are unstable.
- If a public source is deprecated or in transition, label it as method reference rather than current recommended implementation.

Use `references/source-map.md` for source patterns and GitHub projects that informed this skill.
Use `references/release-checklist.md` before finalizing a document.

## Release Readiness Checklist

Before final output, verify:

- Cost numbers reconcile line by line.
- Every scenario compares against the pure manual baseline.
- Long-run savings have explicit quality gates.
- Current state is not overstated as fully launched if data import or production rollout is incomplete.
- Tables have no truncated words or broken cells.
- Claims about models/frameworks have primary-source support and date stamps.
- The recommended plan is visible in the first page.
