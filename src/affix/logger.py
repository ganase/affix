"""追記型プロジェクトログの補助処理。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append_run_logs(log_dir: Path, idea_count: int, draft_count: int) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    _append(
        log_dir / "progress.md",
        f"\n## {timestamp}\n\n"
        f"- {idea_count}件の記事案を生成しました。\n"
        f"- {draft_count}件のMarkdown下書きを書き出しました。\n"
        "- `data/output/` 配下のJSONとCSVを更新しました。\n",
    )
    _append(
        log_dir / "assumptions.md",
        f"\n## {timestamp}\n\n"
        "- 外部ネットワークを使わない前提のため、ローカルCSVを唯一の入力元として扱いました。\n"
        "- 生成されたすべての下書きは、公開前に人間レビューが必要なものとして扱いました。\n"
        "- 安全性、単純さ、テストしやすさを優先して、決定的なテンプレート生成を採用しました。\n",
    )
    _append(
        log_dir / "risks.md",
        f"\n## {timestamp}\n\n"
        "- 下書きには最新の商品変更、価格変更、ポリシー変更が反映されていない可能性があります。\n"
        "- アフィリエイトに関する主張は、公開前に公式情報で確認する必要があります。\n"
        "- 比較記事でランキングや優劣を表現する場合は、事前に根拠が必要です。\n",
    )
    _append(
        log_dir / "next_actions.md",
        f"\n## {timestamp}\n\n"
        "- 生成されたMarkdown下書きを確認し、事実確認項目をチェックしてください。\n"
        "- 実際のキーワード調査結果を `data/input/keywords.csv` に追加してください。\n"
        "- WordPressや静的サイト連携を追加する前に、人間承認つきの公開フローを設計してください。\n",
    )


def _append(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(f"# {path.stem.replace('_', ' ')}\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as file:
        file.write(text)
