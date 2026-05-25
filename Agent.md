# AGENTS.md

## Project goal

This repository is for building an automated affiliate website operation system.

The system should support:
- market research
- keyword research
- article outline generation
- article drafting
- affiliate link management
- WordPress or static site publishing
- periodic content refresh
- logging and review reports

## Working style

Act autonomously as much as possible.

Do not ask the user questions unless:
- credentials, API keys, passwords, or paid service decisions are required
- a destructive action may delete or overwrite important data
- legal, financial, medical, or compliance-sensitive judgment is required
- the task cannot proceed without missing information

If information is missing, make a reasonable assumption and continue.
Record assumptions in `logs/assumptions.md`.

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

## Implementation rules

Prefer small, testable changes.
After each major change:
- run relevant tests
- run lint or format checks if available
- update documentation if behavior changed
- write a short summary in `logs/progress.md`

## Verification

A task is complete only when:
- implementation is done
- tests or smoke checks pass
- generated output is saved
- assumptions are documented
- remaining risks are listed
- next recommended step is written

## Affiliate / SEO safety

Do not generate misleading claims.
Do not invent product features, prices, rankings, reviews, or official endorsements.
When facts are uncertain, mark them as requiring human review.
For YMYL topics such as finance, health, medicine, insurance, legal, or investment, use extra caution and require human review before publishing.

## Communication

At the end of each run, produce:

1. What was done
2. Files changed
3. Tests/checks run
4. Assumptions made
5. Risks or unresolved issues
6. Next actions

Do not stop merely because a better option exists.
Choose a reasonable option, proceed, and document the tradeoff.
