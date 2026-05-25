"""Affixで扱うデータモデル。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Niche:
    niche_id: str
    niche_name: str
    description: str
    monetization_type: str
    ymyl_risk: str
    competition_level: str
    notes: str


@dataclass(frozen=True)
class Keyword:
    keyword_id: str
    niche_id: str
    keyword: str
    search_intent: str
    funnel_stage: str
    article_type: str
    priority: str
    notes: str


@dataclass(frozen=True)
class ArticleIdea:
    article_id: str
    niche_id: str
    niche_name: str
    keyword: str
    search_intent: str
    funnel_stage: str
    article_type: str
    suggested_title: str
    target_reader: str
    article_outline: list[str] = field(default_factory=list)
    affiliate_angle: str = ""
    human_review_required: bool = True
    risk_notes: str = ""
    fact_check_items: list[str] = field(default_factory=list)
