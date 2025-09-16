---
marp: true
theme: default
---
<!-- Mermaidスクリプト読み込み -->
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@latest/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true });
</script>

# コンタクトセンター通話分析システム
## Amazon Bedrock + Claude を活用したVOC分析

---

# システム概要図
<pre class="mermaid">
<!-- ```mermaid -->
graph TD
    A[音声通話テキスト<br>CSVファイル] --> B[Claude API]
    B --> C{機能呼び出し}
    C -->|1| D[顧客要望抽出]
    C -->|2| E[要望達成判定]
    C -->|3| F[判定理由分析]
    C -->|4| G[満足度スコア算出]
    D & E & F & G --> H[構造化データ<br>CSV出力]
<!-- ``` -->
</pre>

---

# システム概要

- Amazon Bedrockを利用してClaude APIと連携
- Function Callingによる構造化された出力の生成
- 自然文を構造化データとして出力

---

# 主な機能と特徴

### 分析機能
1. **顧客要望の抽出** 
   - 通話内容から時系列順に要望をリスト化

2. **要望達成度の判定**
   - 各要望に対する達成/未達成を判定

3. **判定理由の分析**
   - 達成判定の根拠を詳細に説明

4. **満足度スコアリング**
   - 0-100点での定量的な満足度評価
