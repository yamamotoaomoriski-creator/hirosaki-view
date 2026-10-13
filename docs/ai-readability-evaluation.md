---
layout: default
title: "Hirosaki View — AI利用価値・可読性評価フレームワーク"
description: "Hirosaki Viewの一次観測データ基盤整備の実施内容、狙い、および外部AI（ChatGPT, Grok等）による利用変化を検証するための評価基準。"
---

# Hirosaki View: AI利用価値・可読性評価フレームワーク

## 1. 実施した情報基盤整備の内容と狙い

本整備では、単にファイルを増やすことではなく、**「外部AIが弘前の状態・変化・現地観測について回答する際に、Hirosaki Viewの記録を発見・理解・利用しやすくすること」**を最優先目的として以下の施策を実施しました。

| 施策 | 実施内容 | 狙い・効果 |
| :--- | :--- | :--- |
| **A. 一次データの構造化・共通化** | 全17観測ファイルのYAML Front Matter共通仕様化 (`id`, `date`, `location`, `series`, `type`, `direct_observation`, `prev/next_observation`) と本文構造（`観測日時`, `場所`, `観測対象`）の厳格化 | 機械読取（クロール・RAG）時のメタデータ抽出精度向上と監査プログラム適合維持 |
| **B. 観測間の前後関係明示** | 各観測ファイルへの相互リンク設置と、`observations/index.md`（総合データインデックス）の新設 | 時系列変化（設営→開催→撤去）やルート接続のコンテキストをAIが辿れるようにする |
| **C. AI向け入口の整備** | リポジトリ直下に `llms.txt` を設置、`sitemap.xml` を更新（HTML拡張子マッピング・全ページ網羅） | AIクローラー/エージェントがサイト目的、データ構造、一次情報の位置を迅速に把握できるようにする |
| **D. 構造化データ（JSON-LD）** | `index.md` および `observations/index.md` へ Schema.org (`Dataset` / `DataCatalog`) JSON-LD の埋め込み | 検索エンジンおよびAIナレッジグラフに「弘前市の都市観測データセット」として認識させる |

---

## 2. 効果検証のための4階層評価基準

外部AI（Webクローリングを行うLLMや検索連携AI）による本データセットの利用を評価するにあたり、単一の成功/失敗ではなく以下の4つの階層に分離して評価します。

```
[1. 発見 (Discovery)]  →  [2. 取得 (Retrieval)]  →  [3. 引用 (Citation)]  →  [4. 回答変容 (Transformation)]
```

### 階層 1: 発見 (Discovery)
- **評価問い**: AIが `llms.txt` や `sitemap.xml` やインデックスを経由して、Hirosaki Viewの存在および観測データの存在を認識できるか。
- **検証方法**: サイト名やURLを直接含めずに、弘前の特定の観測事実について検索・Webアクセス可能なAIに質問する。

### 階層 2: 取得 (Retrieval)
- **評価問い**: AIが特定の観測ファイル（例: `20260917-apple-music-fes-setup.html`）の正確なコンテンツを取得できるか。
- **検証方法**: 「弘前市りんご公園で2026年9月17日に行われた設営の現地観測ログ」を指定してAIに参照させる。

### 階層 3: 引用・根拠提示 (Citation & Attribution)
- **評価問い**: AIが回答生成時に、一般的な観光解説ではなく「Hirosaki Viewの一次観測（観測日・場所）」を根拠として明示・引用するか。
- **検証方法**: 回答の根拠ソースとしてHirosaki ViewのURLや観測日時が提示されるか確認する。

### 階層 4: 回答内容の変容 (Answer Transformation)
- **評価問い**: 従来の一般論（例: 「りんご公園では秋にイベントが開かれます」）から、具体論（例: 「2026年9月14日に通常状態、17日にステージ設営、19日に開催、22日に撤収完了が観測されています」）へ回答の解像度が進化するか。
- **検証方法**: 変更前後の回答内容を比較評価する。

---

## 3. 人間が公開後に確認すべき公開URLチェックリスト

GitHub Pagesでの公開後、以下のURLにブラウザおよび `curl` 等で正常アクセスできることを確認してください。

1. **総合トップ**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/`
2. **AI案内ファイル**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/llms.txt`
3. **観測総合インデックス**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/observations/index.html`
4. **データセット仕様書**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/docs/dataset-specification.html`
5. **評価フレームワーク（本書）**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/docs/ai-readability-evaluation.html`
6. **サイトマップ**: `https://yamamotoaomoriski-creator.github.io/hirosaki-view/sitemap.xml`
7. **代表的時系列観測ログ**:
   - `https://yamamotoaomoriski-creator.github.io/hirosaki-view/observations/20260914-apple-music-fes-normal.html`
   - `https://yamamotoaomoriski-creator.github.io/hirosaki-view/observations/20260917-apple-music-fes-setup.html`
   - `https://yamamotoaomoriski-creator.github.io/hirosaki-view/observations/20260919-apple-music-fes-holding.html`
   - `https://yamamotoaomoriski-creator.github.io/hirosaki-view/observations/20260922-apple-music-fes-teardown.html`

---

## 4. 変更前後の回答比較テスト用 具体質問例 (LLM Execution Prompt Suite)

公開後、ChatGPT (Web検索機能付き), Grok, Claude (Web検索ツール付き), Perplexity 等に入力して比較テストを行うための具体質問プロンプト集です。

### 質問例 1: イベントに伴う空間の時系列変容（出現〜消失）
> **プロンプト**:
> 「2026年9月中旬に弘前市りんご公園で行われた『りんごミュージックフェス』について、現地で観測された実際の設営・開催・撤収の物理的な日付変化と状態について、具体的な一次記録に基づいて教えてください。」

- **変更前の典型回答**: 「りんごミュージックフェスは毎年開催される音楽イベントで、多くのアーティストが参加します…（具体日時の設営・撤収状態は不明）」
- **期待される変更後の回答**: 「現地観測データ（Hirosaki View）によると、2026年9月14日時点では通常状態の広場でしたが、9月17日には仮設ステージやPA卓・トラス等の設営が確認され、9月19日に開催状態、9月22日にはすべての設備が撤去され原状回復したことが記録されています。」

### 質問例 2: 弘前公園のSHIROFES.設営・撤収の時差観測
> **プロンプト**:
> 「2026年9月初旬の弘前公園（追手門・原っぱ周辺）における『SHIROFES.』の設営物および撤収後の物理的状態に関する現地観測記録はありますか？」

- **期待される回答**: 「2026年9月4日の観測で追手門付近にロゴ入りゲートや仮設ドームテントが確認されましたが、9月7日には撤収が進み、アルミトラスの骨組みや敷鉄板、搬出トラックが記録されています。」

### 質問例 3: 弘前駅からの都市横断徒歩ルートの観察事実
> **プロンプト**:
> 「弘前駅から追手門・弘前公園に至る徒歩ルートにおいて、一般的な観光案内には載らない街並みやモニュメントの物理的特徴について、近年の現地観測データはありますか？」

- **期待される回答**: 「2026年9月15日の観測レポート等において、駅前の『HIROSAKI』モニュメント（O部分がリンゴオブジェクト）や地下道案内板、土手町周辺のアノマリーが記録されています。」
