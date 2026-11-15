Hirosaki View FORMAT_MASTER v1.0

- Status: Draft for implementation
- Version: 1.0
- Purpose: Raw Observationから、AIが検索・比較・分析に利用するStructured Dataを生成するための基準
- Principle: 観測の保存と知識構造の進化を分離する

---

1. 基本構造

Hirosaki Viewのデータは、次の2系統で管理する。

Raw Observation

- 観測時に記録された原本。
- Registerから追加される。
- 再構成処理による変更・上書きは禁止。
- 当時の観測事実、記録者の認識、違和感、推測、未整理の記述を含め、原文を保存する。

Structured Data

- Raw Observationを本FORMAT_MASTERに基づいて再構成したデータ。
- AIによる分類、関係付け、時系列比較、解釈を含む。
- 再生成可能な派生データとして扱う。
- 通常のAI検索・分析ではStructured Dataを主な参照先とする。
- 原文確認、検証、再構成時にはRaw Observationを参照する。

RawとStructuredは物理的に分離する。

---

2. Structured Dataの6項目

2-1. Observation Facts

観測事実を保持する。

対象：

- 観測日時
- 観測場所
- 観測対象
- Rawに記載された物理的状態
- Rawに記載された確認事項

ルール：

- Rawの事実記述を可能な限り原文のまま保持する。
- 要約によって情報を削らない。
- 原文にない事実を追加しない。
- AIによる分類や推論を観測事実に混入させない。
- 複数の記述を分割する場合も、元の意味と関係を保持する。

2-2. Contemporary Context

観測当時の記録者の認識・文脈を保持する。

対象：

- Human observation
- 当時の認識
- 違和感
- 当時の推測や問題意識
- 状態に対する記録者の表現

ルール：

- Rawの表現を可能な限りそのまま保持する。
- 後年のAI解釈で書き換えない。
- Observation Factsと意味が重複しても、当時の認識として重要なら保持する。
- 当時の認識と、現在のAIによる解釈を混同しない。

2-3. Structure

観測内容を検索・比較可能な構造に分類する。

基本区分：

State

- 観測時点の状態。

Change

- 前回観測からの変化。
- Rawに変化の記述がある場合は、その表現を保持する。
- 複数のRawを比較して導出した変化は、比較元の記録を明示する。

Event

- 関連するイベント名と観測されたフェーズ。
- 例：りんごミュージックフェス／設営フェーズ。
- イベント名とフェーズの分類根拠を区別する。

Relationships

- 前後の観測記録。
- 同一シリーズ内の関係。
- 関連する場所・現象・観測記録。
- 関係性を追加する場合は根拠となる記録を明示する。

ルール：

- Structureは検索・比較のための分類であり、Rawそのものではない。
- AIによる分類には、その分類がAIによるものと分かる情報を付ける。
- Rawにない関係性を事実として追加しない。
- 関係性が推定の場合は、確定した関係と区別する。
- 状態・変化・イベントのフェーズを混同しない。

2-4. AI Interpretation

AIによる分類・解釈・推論を保持する。

対象：

- 複数観測から導出した変化
- 状態の意味
- 観測間の関連性
- 現象の可能性
- 後年の視点からの再解釈

必須情報：

- interpretation：解釈内容
- evidence：根拠となるRawまたはStructuredの記述
- confidence：解釈の確からしさ

ルール：

- Observation Factsと明確に分離する。
- 根拠のない推論を追加しない。
- 推論を確定事実として表現しない。
- 複数記録から導出した場合は、参照した記録を明示する。
- 新しい観測によって解釈が変わった場合、過去のRawや当時の認識を書き換えない。

Observation ConfidenceとAI Interpretation Confidenceは別々に扱う。

2-5. Residual

現行の構造に収まらない情報を保護する。

対象：

- 現行項目に分類できない原文
- 現行の分類では意味を十分に表現できない記述
- 曖昧さや違和感
- 解釈が確定できない情報
- 構造化によって失われる可能性のある表現

状態：

status| 意味
empty| 照合済みで、構造外の情報がない
unreviewed| 原文との照合が未完了
unresolved| 情報はあるが意味を確定できない
out_of_schema| 現行構造に収まらない情報がある

ルール：

- Residualを単なる余り物入れにしない。
- 該当情報がある場合は、原文に近い形で保存する。
- 意味を勝手に補完しない。
- 未照合の状態を、情報が存在しない状態として扱わない。
- 空の場合はstatusをemptyとし、entriesを空配列にする。
- Residualの内容を削除する場合は、削除理由と対応先を確認する。

2-6. Provenance

Structured Dataの出所と生成条件を保持する。

対象：

- source_raw
- RawのFront Matter全項目
- Evidence
- Observation Confidence
- 閲覧用ナビゲーション
- generator
- generated_at
- master_version
- 生成に使用したMasterのGit commit

ルール：

- Rawのメタデータを欠落させない。
- 元ファイルへの参照を保持する。
- Evidenceのファイル名を保持する。
- 画像を実際に確認していない場合、画像の内容を推測しない。
- 生成条件を追跡できるようにする。

前後の観測関係はStructureにも保持する。Provenanceのナビゲーションは閲覧導線として保持し、役割を分ける。

---

3. 再構成の禁止事項

再構成AIは以下を行ってはならない。

1. Raw Observationの変更・上書き・削除。
2. Rawに存在しない観測事実の追加。
3. 推論を観測事実として記録すること。
4. 当時の認識を後年の解釈で書き換えること。
5. 曖昧な記述を勝手に確定すること。
6. 原文の強い表現やニュアンスを弱めること。
7. 構造に収まらない情報を黙って捨てること。
8. 根拠のない関連記録や因果関係を追加すること。
9. 画像を確認せず、その画像に写っている内容を補完すること。

情報を分類できない場合は、無理に分類せずResidualに保持する。

---

4. Masterのバージョン管理

Semantic Versioningを使用する。

- PATCH：誤記修正、説明の明確化など、構造・意味を変えない修正。
- MINOR：項目追加、任意属性追加など、既存データとの互換性を維持する拡張。
- MAJOR：既存項目の意味変更、構造変更、既存データの解釈に影響する変更。

変更時は以下を記録する。

- version
- date
- changed_items
- change_reason
- migration_impact

Masterの変更だけで全Structured Dataを自動再生成しない。

対象を指定して再構成する。再構成時には使用したMasterのバージョンとGit commitを記録する。

---

5. 再構成処理の基本フロー

1. 対象Raw Observationを読み込む。
2. FORMAT_MASTERのバージョンを確認する。
3. Rawのメタデータ・本文・リンク・Evidenceを照合する。
4. 6項目に分類する。
5. RawとStructuredの情報対応を確認する。
6. 欠落・創作・意味の変化・未分類情報を検査する。
7. Structured Dataを別の保存先に出力する。
8. GitHub上で差分を確認できる状態にする。

初期運用では1ファイル単位の手動実行を基本とする。

Rawの変更を伴う処理は認めない。

---

6. 初期検証の評価基準

以下を満たすこと。

- Rawのメタデータが全項目保持されている。
- 観測事実が欠落・改変されていない。
- Contemporary Contextが保持されている。
- FactsとAI Interpretationが混同されていない。
- State / Change / Event / Relationshipsが区別されている。
- EvidenceとObservation Confidenceが保持されている。
- AI Interpretationに根拠がある。
- Residualの照合状態が正しく表現されている。
- 前後の観測記録を追跡できる。
- Rawが一切変更されていない。

一つでも重大な情報欠落・創作・意味改変があれば、その再構成結果は採用しない。

---

7. 初期実装方針

- Registerは現行の仕組みを維持する。
- Raw Observationの保存場所は現行の"observations/"を維持する。
- Structured DataはRawと別のディレクトリに保存する。
- 初期検証は1ファイル単位で行う。
- 既存の全観測記録を一括変換しない。
- 生成結果はRawと比較してから採用する。

本Masterの目的は、観測記録を均一な文章に整形することではない。

弘前の物理的な状態・変化・現象を、観測時点の情報を失わずに蓄積し、後年のAIが再解釈・比較・発見できる知識構造へ進化させることである。
