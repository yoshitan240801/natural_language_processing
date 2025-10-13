# Amazon Bedrock・Claude・RAG・LLM を用いた自学自習での自然言語処理ユースケース集

このリポジトリでは、**Amazon Bedrock**、**RAG**、**Gradio** などのツールを使って自学自習で作ってみた自然言語処理のコードを紹介しています。

プロンプトエンジニアリング、構造化出力、UI を含む NLP アプリケーションの構築に関心がある方に適しています。

---

## 🔧 使用技術

- **Amazon Bedrock**（AWS 上の LLM アクセス）
- **Claude（Anthropic）**（大規模言語モデル）
- **ChromaDB**（軽量なベクトルデータベース）
- **LangChain**（LLM 構成フレームワーク）
- **Transformers**（LLM 構成フレームワーク）
- **Gradio**（機械学習アプリのUI作成）
- **Python 3.10 以上**

---

## 📁 ディレクトリ構成

| ディレクトリ名 | 概要 |
|----------------|------|
| [`aws_bedrock`](./aws_bedrock) | Amazon Bedrock を使ったプロンプトエンジニアリングの基礎 |
| [`bedrock_chroma_simple_rag`](./bedrock_chroma_simple_rag) | Chroma + Claude によるシンプルな RAG パイプライン |
| [`bert_classification`](./bert_classification) | Transformersを用いたBERTの文章分類のファインチューニング |
| [`claude_gradio_app`](./claude_gradio_app) | Claude を活用した Gradio ベースのチャットアプリ |
| [`claude_structured_output_usecase`](./claude_structured_output_usecase) | Claude を使った JSON 形式の構造化出力例 |
| [`claude_structured_output_usecase_2`](./claude_structured_output_usecase_2) | より高度な構造化出力ユースケースの実装 |
| [`rinna-gpt2_generate`](./rinna-gpt2_generate) | Transformersを用いたGPT2の文章生成のファインチューニング |
| [`t5_summarize`](./t5_summarize) | Transformersを用いたT5の文章要約のファインチューニング |


---

