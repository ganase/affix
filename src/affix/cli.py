"""Command line interface for Affix."""

from __future__ import annotations

import argparse
from pathlib import Path

from .generator import generate_article_ideas
from .loaders import load_keywords, load_niches
from .logger import append_run_logs
from .writer import write_csv, write_json, write_markdown_drafts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Affix affiliate site operation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate article ideas and review drafts")
    generate.add_argument("--root", type=Path, default=Path.cwd(), help="Project root directory")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        return generate_command(args.root)

    parser.error(f"Unknown command: {args.command}")
    return 2


def generate_command(root: Path) -> int:
    root = root.resolve()
    niches = load_niches(root / "data" / "input" / "niches.csv")
    keywords = load_keywords(root / "data" / "input" / "keywords.csv")
    ideas = generate_article_ideas(niches, keywords)

    output_dir = root / "data" / "output"
    drafts_dir = root / "content" / "drafts"
    write_json(output_dir / "article_ideas.json", ideas)
    write_csv(output_dir / "article_ideas.csv", ideas)
    drafts = write_markdown_drafts(drafts_dir, ideas)
    append_run_logs(root / "logs", idea_count=len(ideas), draft_count=len(drafts))

    print(f"Generated {len(ideas)} article ideas.")
    print(f"Wrote JSON: {output_dir / 'article_ideas.json'}")
    print(f"Wrote CSV: {output_dir / 'article_ideas.csv'}")
    print(f"Wrote drafts: {drafts_dir}")
    print("Updated logs: logs/")
    return 0
