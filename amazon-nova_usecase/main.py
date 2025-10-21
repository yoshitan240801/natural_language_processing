import dotenv
import os

import boto3


BEDROCK_CLIENT = boto3.client("bedrock-runtime",
                              region_name="ap-northeast-1")
dotenv.load_dotenv()
MODEL_ID_AMAZON_NOVA = os.getenv("BEDROCK_AMAZON_NOVA_PRO_MODEL_ID")  # amazon nova pro
SYSTEM_PROMPT = """
あなたはコンタクトセンター業務を効率化するために、通話テキストのフィルタリングを担当するアシスタントです。
以下に与えられた通話ログ（CU: はお客様、OP: はオペレーター）について、次の「除外条件 A〜C」に該当するかを判断してください。
---
【除外条件】
次のいずれかに当てはまる場合は「Yes」、当てはまらない場合は「No」と出力してください。

A. お客様が不在で、オペレーターが留守番電話にメッセージを残しただけで通話が終了している。
- CU の発話が自動音声ガイダンス（例：「お名前とご用件をお話しください」「電話に出ることができません」など）に限定されている。
- OPは自己紹介と簡単な連絡内容を述べ、折り返しを案内して通話が終了している。

B. お客様またはオペレーターの担当者が不在で、用件に関する具体的なやり取りや対応が一切行われなかった。
- 保留状態、担当者不在、名指し人が不在などにより、実質的なコミュニケーションが行われていない。

C. 一時的に会話が発生しているが、内容の確認や処理には至らず、オペレーターが後日折り返すことで通話が終了している。
- CUが「今は対応できない」「後でかけ直してほしい」と発言し、OPが「また改めてご連絡します」として終了している。
- この場合、CUが一言二言応答していても、具体的な説明・手続き・案内・対応・意思確認などが行われていなければ「Yes」と判定してください。
---
【重要な判断指針】
- 除外すべきでない通話とは、CUとOPの間で**明確なやり取り**や**意思確認・対応・説明・案内**が行われている通話です。
- CUが一時的に対応できない状況であっても、その中で何らかの**対応方針が決まった場合（日時確定・対応内容確定など）**は除外対象とはしないでください。
- 曖昧な場合は「No」としてください（※除外しすぎを防ぐため）。
---
【出力形式】
Yes または No のみ
"""


def call_amazon_nova(input_text_data):
    USER_PROMPT = input_text_data
    prompt = """
    {a}
    <text>
    {b}
    </text>
    """.format(a=SYSTEM_PROMPT, b=USER_PROMPT)
    amazon_nova_input_with_prompt = [{"role": "user",
                                      "content": [{"text": prompt}]}]
    amazon_nova_response = BEDROCK_CLIENT.converse(modelId=MODEL_ID_AMAZON_NOVA,
                                                   messages=amazon_nova_input_with_prompt,
                                                   inferenceConfig={"temperature": 0.2})
    amazon_nova_response_text = amazon_nova_response["output"]["message"]["content"][0]["text"]
    return amazon_nova_response_text
