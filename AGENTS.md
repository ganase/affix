# AGENTS.md

## Project goal

This repository builds Affix, a minimal automated affiliate website operation system.

The system should help with:
- market and niche research inputs
- keyword candidate management
- article idea generation
- review-first Markdown draft output
- affiliate angle planning
- logging assumptions, progress, risks, and next actions
- future WordPress, static site, and GitHub Actions integration

Affix must not auto-publish articles without explicit human approval.

## Working style

Act autonomously as much as possible.

Do not stop to ask preference questions.
When there are multiple reasonable options, choose the safest and simplest option, continue, and document the assumption and tradeoff.

If information is missing, make a reasonable assumption and continue.
Record assumptions in `logs/assumptions.md`.

## When to ask the user

Ask the user only when:
- credentials, API keys, passwords, or paid service decisions are required
- a destructive action may delete or overwrite important data
- legal, financial, medical, or compliance-sensitive judgment is required
- the task cannot proceed without missing information

## Decision priority

When choices are ambiguous, decide using this priority:

1. Safety and reversibility
2. Avoiding policy or legal risk
3. Maintainability
4. Simplicity
5. Automation efficiency
6. Performance optimization

## File rules

- Do not edit `.env` directly.
- Do not commit secrets.
- Do not delete existing content unless explicitly instructed.
- Before large refactors, create a backup or a clear diff.
- Store generated research data under `data/`.
- Store generated articles under `content/`.
- Store logs under `logs/`.
- Keep generated drafts review-first and unpublished by default.

## Implementation rules

- Prefer small, testable changes.
- Prefer Python standard library unless a dependency is clearly justified.
- Keep CLI behavior deterministic and easy to smoke test.
- Use structured formats such as CSV and JSON for generated data.
- After each major change, run relevant tests or smoke checks.
- Update documentation when behavior changes.
- Write a short summary in `logs/progress.md`.

## Verification rules

A task is complete only when:
- implementation is done
- tests or smoke checks pass
- generated output is saved
- assumptions are documented
- remaining risks are listed
- next recommended step is written

## Affiliate / SEO safety rules

- Do not generate misleading claims.
- Do not invent prices, rankings, product features, official endorsements, or user reviews.
- Mark uncertain facts as requiring human review.
- For YMYL topics such as finance, health, medicine, insurance, legal, and investment, require human review before publishing.
- Do not auto-publish articles without explicit human approval.
- Keep affiliate angles framed as hypotheses until reviewed.

## Communication format

At the end of each run, produce:

1. What was done
2. Files changed
3. Tests/checks run
4. Assumptions made
5. Risks or unresolved issues
6. Next actions

Do not stop merely because a better option exists.
Choose a reasonable option, proceed, and document the tradeoff.
