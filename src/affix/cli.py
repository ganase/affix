"""Affixのコマンドラインインターフェース。"""

from __future__ import annotations

import argparse
from pathlib import Path

from .generator import generate_article_ideas
from .loaders import load_affiliate_programs, load_keyword_metrics, load_keywords, load_niches
from .logger import append_run_logs
from .writer import write_csv, write_json, write_markdown_drafts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Affix アフィリエイトサイト運営支援CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="記事案とレビュー用下書きを生成します")
    generate.add_argument("--root", type=Path, default=Path.cwd(), help="プロジェクトのルートディレクトリ")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        return generate_command(args.root)

    parser.error(f"不明なコマンドです: {args.command}")
    return 2


def generate_command(root: Path) -> int:
    root = root.resolve()
    niches = load_niches(root / "data" / "input" / "niches.csv")
    keywords = load_keywords(root / "data" / "input" / "keywords.csv")
    affiliate_programs = load_affiliate_programs(root / "data" / "input" / "affiliate_programs.csv")
    keyword_metrics = load_keyword_metrics(root / "data" / "input" / "keyword_metrics.csv")
    ideas = generate_article_ideas(niches, keywords, affiliate_programs, keyword_metrics)

    output_dir = root / "data" / "output"
    drafts_dir = root / "content" / "drafts"
    write_json(output_dir / "article_ideas.json", ideas)
    write_csv(output_dir / "article_ideas.csv", ideas)
    drafts = write_markdown_drafts(drafts_dir, ideas)
    append_run_logs(root / "logs", idea_count=len(ideas), draft_count=len(drafts))

    print(f"{len(ideas)}件の記事案を生成しました。")
    print(f"JSONを書き出しました: {output_dir / 'article_ideas.json'}")
    print(f"CSVを書き出しました: {output_dir / 'article_ideas.csv'}")
    print(f"下書きを書き出しました: {drafts_dir}")
    print("ログを更新しました: logs/")
    return 0
