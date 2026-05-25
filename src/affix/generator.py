"""記事案の生成処理。"""

from __future__ import annotations

import re

from .models import ArticleIdea, Keyword, Niche


YMYL_TERMS = ("金融", "健康", "医療", "保険", "法律", "投資")


def generate_article_ideas(niches: list[Niche], keywords: list[Keyword]) -> list[ArticleIdea]:
    niches_by_id = {niche.niche_id: niche for niche in niches}
    ideas: list[ArticleIdea] = []

    for keyword in keywords:
        niche = niches_by_id.get(keyword.niche_id)
        if niche is None:
            continue
        ideas.append(_build_article_idea(niche, keyword))

    return ideas


def _build_article_idea(niche: Niche, keyword: Keyword) -> ArticleIdea:
    article_id = _make_article_id(niche.niche_id, keyword.keyword_id, keyword.keyword)
    article_type_label = _article_type_label(keyword.article_type)
    suggested_title = f"{keyword.keyword}の基礎と選び方: {article_type_label}"
    target_reader = _target_reader(keyword, niche)
    outline = _outline(keyword, niche)
    affiliate_angle = _affiliate_angle(niche, keyword)
    human_review_required = True
    risk_notes = _risk_notes(niche, keyword)
    fact_check_items = _fact_check_items(niche, keyword)

    return ArticleIdea(
        article_id=article_id,
        niche_id=niche.niche_id,
        niche_name=niche.niche_name,
        keyword=keyword.keyword,
        search_intent=keyword.search_intent,
        funnel_stage=keyword.funnel_stage,
        article_type=keyword.article_type,
        suggested_title=suggested_title,
        target_reader=target_reader,
        article_outline=outline,
        affiliate_angle=affiliate_angle,
        human_review_required=human_review_required,
        risk_notes=risk_notes,
        fact_check_items=fact_check_items,
    )


def _make_article_id(niche_id: str, keyword_id: str, keyword: str) -> str:
    base = keyword_id or keyword
    slug = re.sub(r"[^a-zA-Z0-9_]+", "-", base.strip()).strip("-").lower()
    return f"{niche_id}-{slug or 'article'}"


def _article_type_label(article_type: str) -> str:
    labels = {
        "実践ガイド": "実践ガイド",
        "比較ガイド": "比較ガイド",
        "導入ガイド": "導入ガイド",
        "レビュー下書き": "レビュー下書き",
    }
    return labels.get(article_type, "解説ガイド")


def _target_reader(keyword: Keyword, niche: Niche) -> str:
    if keyword.funnel_stage == "比較検討":
        return f"{niche.niche_name}を比較検討しており、導入判断の材料を探している担当者。"
    if keyword.funnel_stage == "意思決定":
        return f"{niche.niche_name}の導入直前で、リスクと確認事項を整理したい担当者。"
    return f"{niche.niche_name}について学び始め、基本的な進め方を理解したい読者。"


def _outline(keyword: Keyword, niche: Niche) -> list[str]:
    return [
        f"{keyword.keyword}で解決したい課題",
        f"{niche.niche_name}の基本と検討前提",
        "選定時に確認すべきポイント",
        "導入・利用時の注意点",
        "候補サービスや関連ツールを見る前のチェック項目",
        "人間レビューで確認すべき事実関係",
    ]


def _affiliate_angle(niche: Niche, keyword: Keyword) -> str:
    if keyword.article_type == "比較ガイド":
        return f"{niche.monetization_type}につながる比較検討導線。ただし順位や優劣は根拠確認後に限定する。"
    if keyword.article_type in {"実践ガイド", "導入ガイド"}:
        return f"{niche.monetization_type}につながる導入支援・関連ツール紹介導線。価格や機能は公式確認後に記載する。"
    return f"{niche.monetization_type}につながる補助導線。読者利益と開示を優先する。"


def _risk_notes(niche: Niche, keyword: Keyword) -> str:
    notes = [
        "生成内容は下書きであり、公開前に必ず人間が確認する必要があります。",
        "根拠のない価格、ランキング、機能説明、公式推薦、利用者レビューは追加しないでください。",
    ]
    risk_text = f"{niche.ymyl_risk} {niche.description} {keyword.keyword} {keyword.notes}".lower()
    if niche.ymyl_risk in {"中", "高"} or any(term in risk_text for term in YMYL_TERMS):
        notes.append("コンプライアンスまたはYMYL隣接リスクがあるため、追加の人間レビューが必要です。")
    if niche.notes:
        notes.append(f"ジャンルメモ: {niche.notes}")
    if keyword.notes:
        notes.append(f"キーワードメモ: {keyword.notes}")
    return " ".join(notes)


def _fact_check_items(niche: Niche, keyword: Keyword) -> list[str]:
    return [
        "公式の商品名またはサービス名",
        "現在の価格とプラン提供状況",
        "現在提供されている機能",
        "アフィリエイトプログラムの規約と開示要件",
        f"「{keyword.keyword}」に関する主張",
        f"{niche.niche_name}のリスク区分: {niche.ymyl_risk}",
    ]
