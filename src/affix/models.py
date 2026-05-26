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
class AffiliateProgram:
    program_id: str
    niche_id: str
    service_name: str
    asp_name: str
    reward_type: str
    reward_amount: str
    approval_condition: str
    cookie_days: str
    official_url: str
    affiliate_url_placeholder: str
    notes: str


@dataclass(frozen=True)
class KeywordMetric:
    keyword_id: str
    search_volume: str
    competition_level: str
    commercial_intent: str
    priority_score: str
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
    program_id: str = ""
    service_name: str = ""
    asp_name: str = ""
    reward_type: str = ""
    reward_amount: str = "TBD"
    approval_condition: str = "TBD"
    cookie_days: str = "TBD"
    official_url: str = ""
    affiliate_url_placeholder: str = "TBD"
    search_volume: str = "TBD"
    keyword_competition_level: str = "TBD"
    commercial_intent: str = "TBD"
    priority_score: str = "0"
    priority_reason: str = ""
    human_review_required: bool = True
    risk_notes: str = ""
    fact_check_items: list[str] = field(default_factory=list)
