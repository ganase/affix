from __future__ import annotations

import csv
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from affix.cli import generate_command


def _score_value(value: str) -> int:
    match = re.search(r"\d+", value or "")
    if match is None:
        return 0
    return int(match.group(0))


class SmokeTest(unittest.TestCase):
    def test_generate_writes_expected_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            shutil.copytree(ROOT / "data" / "input", project / "data" / "input")
            (project / "logs").mkdir(parents=True)

            result = generate_command(project)

            self.assertEqual(result, 0)
            json_path = project / "data" / "output" / "article_ideas.json"
            csv_path = project / "data" / "output" / "article_ideas.csv"
            drafts = sorted((project / "content" / "drafts").glob("*.md"))

            self.assertTrue(json_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertGreaterEqual(len(drafts), 5)

            ideas = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(ideas), 5)
            self.assertIn("article_id", ideas[0])
            self.assertIn("reward_amount", ideas[0])
            self.assertIn("commercial_intent", ideas[0])
            self.assertIn("priority_score", ideas[0])
            scores = [_score_value(idea["priority_score"]) for idea in ideas]
            self.assertEqual(scores, sorted(scores, reverse=True))
            self.assertTrue(ideas[0]["human_review_required"])

            with csv_path.open("r", encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), len(ideas))

            draft_text = drafts[0].read_text(encoding="utf-8")
            self.assertIn("## 公開前チェックリスト", draft_text)
            self.assertIn("## 事実確認が必要な項目", draft_text)
            self.assertIn("## 想定案件", draft_text)
            self.assertIn("## 成果条件", draft_text)
            self.assertIn("## 優先度理由", draft_text)

            progress = project / "logs" / "progress.md"
            self.assertIn("記事案を生成しました", progress.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
