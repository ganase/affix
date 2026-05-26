"""記事案の生成処理。"""

from __future__ import annotations

import re

from .models import AffiliateProgram, ArticleIdea, Keyword, KeywordMetric, Niche


YMYL_TERMS = ("金融", "医療", "健康", "保険", "法律", "投資")


def generate_article_ideas(
    niches: list[Niche],
    keywords: list[Keyword],
    affiliate_programs: list[AffiliateProgram],
    keyword_metrics: list[KeywordMetric],
) -> list[ArticleIdea]:
    niches_by_id = {niche.niche_id: niche for niche in niches}
    programs_by_niche_id = _programs_by_niche_id(affiliate_programs)
    metrics_by_keyword_id = {metric.keyword_id: metric for metric in keyword_metrics}
    ideas: list[ArticleIdea] = []

    for keyword in keywords:
        niche = niches_by_id.get(keyword.niche_id)
        if niche is None:
            continue
        program = programs_by_niche_id.get(niche.niche_id)
        metric = metrics_by_keyword_id.get(keyword.keyword_id)
        ideas.append(_build_article_idea(niche, keyword, program, metric))

    return sorted(ideas, key=lambda idea: _score_value(idea.priority_score), reverse=True)


def _programs_by_niche_id(programs: list[AffiliateProgram]) -> dict[str, AffiliateProgram]:
    programs_by_niche_id: dict[str, AffiliateProgram] = {}
    for program in programs:
        programs_by_niche_id.setdefault(program.niche_id, program)
    return programs_by_niche_id


def _build_article_idea(
    niche: Niche,
    keyword: Keyword,
    program: AffiliateProgram | None,
    metric: KeywordMetric | None,
) -> ArticleIdea:
    article_id = _make_article_id(niche.niche_id, keyword.keyword_id, keyword.keyword)
    article_type_label = _article_type_label(keyword.article_type)
    suggested_title = f"{keyword.keyword}の基礎と選び方: {article_type_label}"
    target_reader = _target_reader(keyword, niche)
    outline = _outline(keyword, niche)
    affiliate_angle = _affiliate_angle(niche, keyword, program)
    human_review_required = _requires_human_review(niche, keyword, program)
    risk_notes = _risk_notes(niche, keyword, program, metric)
    fact_check_items = _fact_check_items(niche, keyword, program, metric)

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
        program_id=program.program_id if program else "",
        service_name=program.service_name if program else "TBD",
        asp_name=program.asp_name if program else "TBD",
        reward_type=program.reward_type if program else "TBD",
        reward_amount=program.reward_amount if program else "TBD",
        approval_condition=program.approval_condition if program else "TBD",
        cookie_days=program.cookie_days if program else "TBD",
        official_url=program.official_url if program else "",
        affiliate_url_placeholder=program.affiliate_url_placeholder if program else "TBD",
        search_volume=metric.search_volume if metric else "TBD",
        keyword_competition_level=metric.competition_level if metric else "TBD",
        commercial_intent=metric.commercial_intent if metric else "TBD",
        priority_score=metric.priority_score if metric else "0",
        priority_reason=_priority_reason(keyword, metric),
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


def _affiliate_angle(niche: Niche, keyword: Keyword, program: AffiliateProgram | None) -> str:
    program_text = ""
    if program is not None:
        program_text = f" 想定案件は「{program.service_name}」({program.asp_name})。報酬額と条件はサンプルまたはTBDとして扱う。"
    if keyword.article_type == "比較ガイド":
        return f"{niche.monetization_type}につながる比較検討導線。ただし順位や優劣は根拠確認後に限定する。{program_text}"
    if keyword.article_type in {"実践ガイド", "導入ガイド"}:
        return f"{niche.monetization_type}につながる導入支援・関連ツール紹介導線。価格や機能は公式確認後に記載する。{program_text}"
    return f"{niche.monetization_type}につながる補助導線。読者利益と開示を優先する。{program_text}"


def _requires_human_review(niche: Niche, keyword: Keyword, program: AffiliateProgram | None) -> bool:
    risk_text = _risk_text(niche, keyword, program)
    if any(term in risk_text for term in YMYL_TERMS):
        return True
    return True


def _risk_notes(
    niche: Niche,
    keyword: Keyword,
    program: AffiliateProgram | None,
    metric: KeywordMetric | None,
) -> str:
    notes = [
        "生成内容は下書きであり、公開前に必ず人間が確認する必要があります。",
        "根拠のない価格、ランキング、機能説明、公式推薦、利用者レビューは追加しないでください。",
    ]
    risk_text = _risk_text(niche, keyword, program)
    if niche.ymyl_risk in {"中", "高"} or any(term in risk_text for term in YMYL_TERMS):
        notes.append("コンプライアンスまたはYMYL隣接リスクがあるため、追加の人間レビューが必要です。")
    if program is not None:
        notes.append("案件情報はサンプルまたはTBDを含むため、ASP管理画面で確認してから公開してください。")
    if metric is not None:
        notes.append("キーワード評価はサンプル値を含むため、実データに置き換えてから優先順位を確定してください。")
    if niche.notes:
        notes.append(f"ジャンルメモ: {niche.notes}")
    if keyword.notes:
        notes.append(f"キーワードメモ: {keyword.notes}")
    return " ".join(notes)


def _fact_check_items(
    niche: Niche,
    keyword: Keyword,
    program: AffiliateProgram | None,
    metric: KeywordMetric | None,
) -> list[str]:
    items = [
        "公式の商品名またはサービス名",
        "現在の価格とプラン提供状況",
        "現在提供されている機能",
        "アフィリエイトプログラムの規約と開示要件",
        f"「{keyword.keyword}」に関する主張",
        f"{niche.niche_name}のリスク区分: {niche.ymyl_risk}",
    ]
    if program is not None:
        items.append(f"ASP案件「{program.service_name}」の提携可否、成果条件、報酬額")
    if metric is not None:
        items.append(f"キーワード評価の根拠: 検索ボリューム {metric.search_volume} / 優先度 {metric.priority_score}")
    return items


def _priority_reason(keyword: Keyword, metric: KeywordMetric | None) -> str:
    if metric is None:
        return "キーワード評価データがないため、優先度は0として扱います。"
    return (
        f"優先度スコア {metric.priority_score}、商用意図 {metric.commercial_intent}、"
        f"競合 {metric.competition_level}、検索ボリューム {metric.search_volume} をもとに並べ替えます。"
    )


def _risk_text(niche: Niche, keyword: Keyword, program: AffiliateProgram | None) -> str:
    program_text = ""
    if program is not None:
        program_text = (
            f" {program.service_name} {program.reward_type} {program.approval_condition} {program.notes}"
        )
    return f"{niche.ymyl_risk} {niche.description} {niche.notes} {keyword.keyword} {keyword.notes}{program_text}"


def _score_value(priority_score: str) -> int:
    match = re.search(r"\d+", priority_score or "")
    if match is None:
        return 0
    return int(match.group(0))
