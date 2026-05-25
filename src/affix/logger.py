"""Append-only project log helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append_run_logs(log_dir: Path, idea_count: int, draft_count: int) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    _append(
        log_dir / "progress.md",
        f"\n## {timestamp}\n\n"
        f"- Generated {idea_count} article ideas.\n"
        f"- Wrote {draft_count} Markdown drafts.\n"
        "- Updated JSON and CSV outputs under `data/output/`.\n",
    )
    _append(
        log_dir / "assumptions.md",
        f"\n## {timestamp}\n\n"
        "- Used local CSV files as the source of truth because external network access is disabled.\n"
        "- Treated every generated draft as requiring human review before publication.\n"
        "- Chose deterministic template-based generation for safety, simplicity, and testability.\n",
    )
    _append(
        log_dir / "risks.md",
        f"\n## {timestamp}\n\n"
        "- Drafts may omit recent product changes, pricing changes, or policy changes.\n"
        "- Affiliate claims must be checked against official sources before publication.\n"
        "- Comparison articles need evidence before using rankings or superiority claims.\n",
    )
    _append(
        log_dir / "next_actions.md",
        f"\n## {timestamp}\n\n"
        "- Review generated Markdown drafts and mark fact-check items.\n"
        "- Add real keyword research exports to `data/input/keywords.csv`.\n"
        "- Design a human-approved publishing workflow before adding WordPress or static site automation.\n",
    )


def _append(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(f"# {path.stem.replace('_', ' ').title()}\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as file:
        file.write(text)
