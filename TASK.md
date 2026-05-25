# TASK.md

## Implementation scope

Build the first minimal Affix development foundation for an automated affiliate website operation system.

This implementation creates:
- project guidance for future autonomous Codex work
- safe Codex project configuration notes
- sample niche and keyword input CSV files
- a standard-library-only Python CLI
- article idea JSON and CSV output
- review-oriented Markdown drafts
- assumption, progress, risk, and next-action logs
- a smoke test that verifies the core generator flow

## Completed behavior

Running:

```bash
python run_affix.py generate
```

will:

1. Read `data/input/niches.csv`
2. Read `data/input/keywords.csv`
3. Generate article ideas by combining matching niches and keywords
4. Save `data/output/article_ideas.json`
5. Save `data/output/article_ideas.csv`
6. Write Markdown drafts under `content/drafts/`
7. Append progress to `logs/progress.md`
8. Append assumptions to `logs/assumptions.md`
9. Append risks to `logs/risks.md`
10. Append recommended next actions to `logs/next_actions.md`

## Completion conditions

The current task is complete when:
- the listed directory structure exists
- the CLI runs without external dependencies
- sample input data is present
- JSON, CSV, and Markdown outputs are generated
- smoke tests pass
- logs document assumptions, risks, progress, and next actions

## Intentional non-goals

- No automatic publishing
- No WordPress API calls
- No external keyword volume lookup
- No affiliate network API integration
- No paid service dependency
- No secret handling
