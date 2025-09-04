# このフォルダのプログラムについて

このフォルダのプログラム(main.ipynb)は、langchainライブラリーで<br>

- Embeddingと文章生成のLLMとしてAWS Bedrockのモデル<br>
- ベクトルDBとしてChroma<br>

を用いてシンプルなRAGを実装したものです。

## 概要

main.ipynbは下記の関数で構成されています。<br>

1. set_llm_model_and_vector_db<br>　⇒BedrockのLLMを設定 & ChromaベクトルDBを新規作成もしくは再読み込みします。<br>
2. get_chunked_document_from_csv<br>　⇒csvファイルの対象のカラムを読み込んだ後にチャンク化します。<br>
3. embedding_process<br>　⇒チャンク化したドキュメントをベクトル化します。<br>
4. add_doc_and_vector_in_vector_db<br>　⇒チャンク化したドキュメント、ベクトル、一意なIDをベクトルDBに追加します。<br>
5. carry_out_rag_and_llm<br>　⇒プロンプトに対してRAG & LLMで文章生成を行います。<br>

main関数を呼び出す際に、引数update_vector_db_flagにTrueを設定すると1⇒2⇒3⇒4⇒5の順番で実行され、Falseを設定すると1⇒5の順番で実行します。<br>
(作成時のlangchainライブラリーのバージョン： 0.3.27)