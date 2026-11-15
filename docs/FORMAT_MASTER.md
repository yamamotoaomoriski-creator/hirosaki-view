---
master_version: "1.0.0"
updated_at: "2026-11-15"
schema_name: "Hirosaki View Structured Observation Schema"
---

# FORMAT_MASTER v1.0 — Hirosaki View 知識構造定義書

本ドキュメントは、`observations/raw/` に保存された不変の原観測データを、検索・分析・再解釈可能な `observations/structured/` へ再構成するための基準である。

## 1. AI再構成の絶対原則（ガードレール）
1. **事実の不変性:** 原観測データ（Raw）に記載された日時・場所・数値・物理的事象を改変・捏造してはならない。
2. **補完の禁止:** 原文に記載がない情報（天候、温度、背景事情など）を推測で補ってはならない。該当情報がない項目は原則として `null` とする。
3. **認識の分離:** 観測当時の記録者の主観・違和感は「当時認識（Contemporary Context）」に固定し、最新マスターに基づくAIの分析は「AI解釈（AI Interpretation）」に分離する。
4. **情報の非廃棄:** 本フォーマットのどの項目にも当てはまらない記述や曖昧な表現は、要約せず原文のまま「残余（Residual）」へ退避させる。捨てることは厳禁とする。

---

## 2. 6項目構造仕様（Structured Markdown）

生成するファイルは、以下の **YAMLフロントマター** と **6つの本文セクション** で構成する。

### A. YAMLフロントマター（検索・メタデータ）
- `id` [必須 / String]: 原記録の観測ID
- `source_raw` [必須 / String]: 参照元Rawファイルの相対パス
- `master_version` [必須 / String]: 使用したMasterバージョン（例: `"1.0.0"`）
- `reconstructed_at` [必須 / String]: 再構成を実行した日時（ISO 8601）
- `observed_at` [必須 / String]: 原記録の観測日時
- `title` [必須 / String]: 原記録のタイトル
- `series` [任意 / String | null]: シリーズ名
- `location` [必須 / Object]: `area` と `spot`
- `confidence` [必須 / Object]: 信頼度情報

### B. 本文セクション構成（6項目）

1. **`Observation Facts`（観測事実）**
   - 原観測から確認できる客観的事実のみを抽出する。評価や推測は含めない。
2. **`Contemporary Context`（当時認識）**
   - 観測当時に記録者が抱いた疑問、違和感、仮説を当時の文脈のまま保持する。後年の知識で上書きしない。
3. **`Structure`（構造）**
   - 状態、変化、イベント、関係性（前後の観測リンク等）を整理する。
4. **`AI Interpretation`（AI解釈）**
   - 現在の知識構造に基づくAIの解釈。推測と事実を区別し、必ずevidence（根拠）を示す。
5. **`Residual`（残余）**
   - 既存項目に収まらない情報、曖昧さ、未解決事項を原文に近い形で保持する。該当情報がない場合は `null` とする。
6. **`Provenance`（出所・履歴）**
   - Rawの参照先、Masterバージョン、生成日時、オブザーバー、証拠画像などのメタデータを保持する。

---

## 3. 変更履歴（Changelog）
- **v1.0.0 (2026-11-15):** 初期知識構造の正式版確立。6項目構造とガードレールの定義。
