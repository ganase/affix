# TASK.md

## 実装範囲

アフィリエイトサイト自動運営システムであるAffixの、最初の最小開発基盤を作成します。

今回の実装には次を含みます。

- 今後の自律的なCodex作業に向けたプロジェクト方針
- 安全寄りのCodexプロジェクト設定メモ
- サンプルのジャンルCSVとキーワードCSV
- Python標準ライブラリだけで動くCLI
- 記事案のJSON/CSV出力
- レビュー前提のMarkdown下書き
- 仮定、進捗、リスク、次アクションのログ
- 主要な生成フローを確認するスモークテスト

## 実装済みの挙動

次を実行します。

```bash
python run_affix.py generate
```

実行すると、次を行います。

1. `data/input/niches.csv` を読み込む
2. `data/input/keywords.csv` を読み込む
3. 紐づくジャンルとキーワードから記事案を生成する
4. `data/output/article_ideas.json` を保存する
5. `data/output/article_ideas.csv` を保存する
6. `content/drafts/` にMarkdown下書きを書き出す
7. `logs/progress.md` に進捗を追記する
8. `logs/assumptions.md` に仮定を追記する
9. `logs/risks.md` にリスクを追記する
10. `logs/next_actions.md` に次の推奨作業を追記する

## 完了条件

現在のタスクは、次を満たしたときに完了とします。

- 想定したディレクトリ構成が存在する
- CLIが外部依存なしで動作する
- サンプル入力データが存在する
- JSON、CSV、Markdownの出力が生成される
- スモークテストが通る
- ログに仮定、リスク、進捗、次アクションが記録される

## 今回は実装しないこと

- 自動公開
- WordPress API呼び出し
- 外部キーワードボリューム取得
- アフィリエイトネットワークAPI連携
- 有料サービス依存
- 秘密情報の取り扱い
