"""Affixの出力ファイルを書き込む処理。"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict
from pathlib import Path

from .models import ArticleIdea


ARTICLE_FIELDS = [
    "article_id",
    "niche_id",
    "niche_name",
    "keyword",
    "search_intent",
    "funnel_stage",
    "article_type",
    "suggested_title",
    "target_reader",
    "article_outline",
    "affiliate_angle",
    "human_review_required",
    "risk_notes",
]


def write_json(path: Path, ideas: list[ArticleIdea]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(idea) for idea in ideas]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, ideas: list[ArticleIdea]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=ARTICLE_FIELDS, lineterminator="\n")
        writer.writeheader()
        for idea in ideas:
            row = asdict(idea)
            row["article_outline"] = " | ".join(idea.article_outline)
            row["human_review_required"] = "はい" if idea.human_review_required else "いいえ"
            writer.writerow({field: row[field] for field in ARTICLE_FIELDS})


def write_markdown_drafts(directory: Path, ideas: list[ArticleIdea]) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for idea in ideas:
        path = directory / f"{_safe_filename(idea.article_id)}.md"
        path.write_text(render_markdown_draft(idea), encoding="utf-8")
        paths.append(path)
    return paths


def render_markdown_draft(idea: ArticleIdea) -> str:
    outline = "\n".join(f"- {item}" for item in idea.article_outline)
    fact_checks = "\n".join(f"- [ ] {item}" for item in idea.fact_check_items)

    return f"""# {idea.suggested_title}

## 想定読者

{idea.target_reader}

## 検索意図

{idea.search_intent}

## 収益導線

{idea.affiliate_angle}

## 注意事項

{idea.risk_notes}

## 見出し案

{outline}

## 本文ドラフトのたたき台

この記事では「{idea.keyword}」について、読者が検討前に整理すべき前提、確認すべきポイント、導入時の注意点をまとめます。

まず、読者が解決したい課題を明確にします。次に、候補となるサービスや手段を比較する前に、利用目的、運用体制、予算、セキュリティ、サポート条件を確認します。

収益導線は、読者の意思決定を助ける関連サービスや導入支援への案内として設計します。ただし、価格、機能、ランキング、口コミ、公式認定のような事実表現は、公開前に必ず根拠を確認します。

## 人間レビュー項目

- [ ] 誤解を招く表現がない
- [ ] アフィリエイト開示が必要な箇所を確認した
- [ ] 読者に不利益な誘導がない
- [ ] YMYLまたはコンプライアンス上の懸念を確認した
- [ ] 自動公開せず、公開前承認を受ける

## 事実確認が必要な項目

{fact_checks}

## 公開前チェックリスト

- [ ] 公式情報で価格と機能を確認した
- [ ] 根拠のないランキングや断定表現を削除した
- [ ] 必要なアフィリエイト表記を追加した
- [ ] 古い情報や不確かな表現に注記した
- [ ] 人間の最終レビューが完了した
"""


def _safe_filename(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-")
    return safe or "記事"
