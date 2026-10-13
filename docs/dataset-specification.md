---
layout: default
title: "Hirosaki View — データセット仕様書 (Dataset Specification)"
description: "Hirosaki View の一次観測データ集合におけるスキーマ、記録方法、証拠構造および限界定義。"
---

# Hirosaki View データセット仕様書

## 1. データセット概要

Hirosaki View は、弘前市の物理的空間・都市構造・イベントに伴う一時的設置物・時系列変化を人間が現地で直接観測し、機械可読な一次データ（Markdown + Front Matter + 写真証拠）として蓄積するオープンデータセットです。

- **データセット名**: Hirosaki View Primary Urban Observation Dataset
- **対象領域**: 日本国青森県弘前市全域（弘前公園、弘前駅前〜土手町エリア、りんご公園、岩木山神社、青森県武道館等）
- **観測主体**: Hirosaki View Project (現地直接観測)
- **ライセンス**: Creative Commons Zero (CC0 1.0 Universal / Public Domain Dedication)
- **Source of Truth**: リポジトリ内 `observations/` ディレクトリ配下の `.md` ファイル群

---

## 2. Front Matter スキーマ定義

各観測ファイル (`observations/YYYYMMDD-slug.md`) は、冒頭に以下のYAML Front Matterを保持します。

| フィールド | 型 | 必須 | 説明 | 記述例 |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | ✓ | 観測記録のユニーク識別子 (`hv-YYYYMMDD-slug`) | `hv-20260917-apple-music-fes-setup` |
| `date` | Date | ✓ | 観測年月日 (ISO 8601: `YYYY-MM-DD`) | `2026-09-17` |
| `location` | String | ✓ | 観測地点識別子 | `apple-park`, `hirosaki-park`, `station-to-otemon` |
| `title` | String | ✓ | 観測記録の正式名称 | `弘前市りんご公園・設置物観測（設営状態）` |
| `series` | String | - | 関連する時系列観測シリーズ識別子 | `apple-music-fes`, `shirofes`, `urban-routes` |
| `type` | String | ✓ | 観測種別 (`fixed-point`, `route`, `event-setup`, `event-holding`, `event-teardown`) | `event-setup` |
| `observer` | String | ✓ | 観測実施者名 | `Hirosaki-View` |
| `direct_observation` | Boolean | ✓ | 現地直接観測であるかフラグ | `true` |
| `prev_observation` | String | - | シリーズ内の1つ前の観測記録ファイル名 | `20260914-apple-music-fes-normal.md` |
| `next_observation` | String | - | シリーズ内の1つ後の観測記録ファイル名 | `20260919-apple-music-fes-holding.md` |

---

## 3. 観測種別 (Observation Types)

1. **`fixed-point` (定点観測)**: 特定の物理的地点・構造物を指定日時に観測。
2. **`route` (ルート横断観測)**: 一定の移動経路に沿って連続的な空間テクスチャやアノマリーを収集。
3. **`event-setup` (設営観測)**: イベント開催前の資材搬入・仮設インフラ構築状態の記録。
4. **`event-holding` (開催・利用観測)**: イベント本番中の仮設インフラフル稼働状態の記録。
5. **`event-teardown` (撤収・原状回復観測)**: イベント終了後の解体・資材搬出および空間復旧状態の記録。

---

## 4. 観測本文の構造規約

各ファイル本文は以下の標準見出し構造を保持します（機械可読性および自動監査プログラム互換性維持のため）。

```markdown
# [観測タイトル]

## 観測概要
- **観測日時**: YYYY-MM-DD
- **場所**: [観測地点の具体名]
- **観測対象**: [観測対象の具体名]

## 観測事実 (Observation)
- 現地で直接視覚・物理的に確認された客観的事実を箇条書きで記録。

## 空間的変容 (Change / Transition)
- 前回観測からの変化、出現、消失、原状回復などの相転移。

## Human observation / 解釈
- 観測者による定性的所見、空間的文脈、構造的考察（「観測事実」とは明確に区別）。

## Evidence
- 観測時の写真ファイル名（`2812.jpg` 等）や検証用データ。

---
## 観測間ナビゲーション / 関連リンク
- **前回の観測記録**: [通常状態](../observations/20260914-apple-music-fes-normal.md)
- **次回の観測記録**: [開催状態](../observations/20260919-apple-music-fes-holding.md)
- **観測インデックス**: [観測カタログ](../observations/index.md)
```

---

## 5. データの検証性と限界 (Limitations)

- **客観的事実と解釈の分離**: 本データセットは現地で直接確認された「事実」を重視し、観光的・感情的な解釈を排除します。
- **推測の排除**: 観測時に確認できなかった過去の正確な時間、非公開の設計仕様、将来の予定確定情報等は推測で埋めず未確認として扱います。
- **時空間の非連続性**: 観測が行われていない期間について、「連続して変化がなかった」とみなしてはなりません。観測データが存在する日時のみを事実空間とします。
