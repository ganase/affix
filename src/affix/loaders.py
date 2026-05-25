"""CSV読み込み用の補助処理。"""

from __future__ import annotations

import csv
from pathlib import Path

from .models import Keyword, Niche


NICHE_FIELDS = [
    "niche_id",
    "niche_name",
    "description",
    "monetization_type",
    "ymyl_risk",
    "competition_level",
    "notes",
]

KEYWORD_FIELDS = [
    "keyword_id",
    "niche_id",
    "keyword",
    "search_intent",
    "funnel_stage",
    "article_type",
    "priority",
    "notes",
]


def _read_dicts(path: Path, required_fields: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"必須の入力CSVが見つかりません: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing = [field for field in required_fields if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} に必須列がありません: {', '.join(missing)}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def load_niches(path: Path) -> list[Niche]:
    return [Niche(**{field: row[field] for field in NICHE_FIELDS}) for row in _read_dicts(path, NICHE_FIELDS)]


def load_keywords(path: Path) -> list[Keyword]:
    return [Keyword(**{field: row[field] for field in KEYWORD_FIELDS}) for row in _read_dicts(path, KEYWORD_FIELDS)]
