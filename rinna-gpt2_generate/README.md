# このフォルダのプログラムについて

このフォルダのmainプログラム(main.ipynb)は、Hugging Faceのtransformersライブラリーの勉強を兼ねて、rinna社のGPTモデルにて文章生成と、Fine Tuningと、Fine Tuning後での文章生成を試してみたものになります。<br>


---

# プログラムの全体構成

```mermaid
graph TD
    A[事前学習済みモデルのロード] --> B[初期テキスト生成]
    B --> C[学習データの収集・前処理]
    C --> D[Fine Tuning実行]
    D --> E[Fine Tuning後のモデル保存]
    E --> F[Fine Tuning後のテキスト生成]
```

---

## 1. 事前学習済みモデルのロードと初期テキスト生成

**使用モデル**
- モデル: `rinna/japanese-gpt2-medium`
- タスク: 因果的言語モデル (Causal Language Model)

**初期テキスト生成の設定**
- 入力プロンプト: "お勧めのライフハックと言えば、"
- 生成パラメータ:
  - 最大長: 100トークン
  - 最小長: 20トークン
  - 生成文章数: 3つ
  - サンプリング手法: Top-k (500) + Top-p (0.95)

---

## 2. 学習データの収集と前処理

**データソース**
- データセット: ldcc-20140209 (livedoorニュースコーパス)
- 対象カテゴリ: `it-life-hack`

**データ処理フロー**

```mermaid
graph LR
    A[テキストファイル] --> B[タイトル抽出]
    B --> C[DataFrame作成]
    C --> D[シャッフル]
    D --> E[train 80%]
    D --> F[valid 20%]
    E --> G[train.csv]
    F --> H[valid.csv]
    G --> I[train_sentence.txt]
```

---

## 3. Fine Tuning実行フロー

```mermaid
graph TD
    A[事前学習済みモデル] --> B[Trainerの初期化]
    C[学習データセット] --> B
    D[学習パラメータ] --> B
    B --> E[Fine Tuning実行]
    E --> F[モデル保存]
    E --> G[学習状態保存]
    F --> H[./GPT-model-after-FineTuning]
```

**主要な学習設定**
- 学習率: 2e-5、重み減衰: 0.01
- バッチサイズ: 8、エポック数: 3
- block_size: 128トークン、FP16精度

---
