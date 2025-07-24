import json
import boto3


BEDROCK_CLIENT = boto3.client(service_name="bedrock-runtime",
                              region_name="ap-northeast-1")
MODELID_CLAUDE = "anthropic.claude-3-5-sonnet-20240620-v1:0"
CLAUDE_TOOL_NAME = "evaluate_comment"
CLAUDE_TOOL_DEFINITION = {
    "toolSpec": {
        "name": CLAUDE_TOOL_NAME,
        "description": "this prompt check enquete comment and evaluate passion.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "sentiment_label": {
                        "type": "string",
                        "description": """
                            キャンペーン当選にかける熱意のレベルを表します。
                            返答は必ず '非常にある', 'ある', 'ない' のいずれかのみで返答します。
                            (以下が判定条件)
                            ・手間暇をかけて当選したいという思いを綴っている。（重要度：高）
                            以上の条件にあてはまる強度を総合して判断する
                            どれか一つに当てはまるだけでは高い熱意と判断せず、
                            複数の条件を満たした組み合わせに良い評価を下すように調整すること
                        """,
                        "enum": ["非常にある",
                                 "ある",
                                 "ない"]
                    },
                    "sentiment_label_reason": {
                        "type": "string",
                        "description": "判断した根拠を箇条書き(複数の場合は・で分ける)で記述",
                    },
                    "positive_score": {
                        "type": "number",
                        "description": "指定された条件に基づき判断したキャンペーン当選への熱意を数値で表す(0-100)",
                    },
                    "negative_score": {
                        "type": "number",
                        "description": "ネガティブな感情のスコア(0-100)"
                    }
                },
                "required": ["sentiment_label",
                             "sentiment_label_explanation",
                             "positive_score",
                             "negative_score"]
            }
        }
    }
}


def lambda_handler(event, context):
    # TODO implement
    print(event)
    in_data_text = event["in_text"]
    print(in_data_text)
    try:
        claude_prompt = "<text>\n{a}\n</text>\n\n{b} ツールのみを利用すること。".format(a=in_data_text, b=CLAUDE_TOOL_NAME)
        claude_message = [{"role": "user",
                           "content": [{"text": claude_prompt}]}]
        response = BEDROCK_CLIENT.converse(modelId=MODELID_CLAUDE,
                                           messages=claude_message,
                                           toolConfig={"tools": [CLAUDE_TOOL_DEFINITION],
                                                       "toolChoice": {"tool": {"name": CLAUDE_TOOL_NAME}}})
        response_content = response["output"]["message"]["content"][0]["toolUse"]["input"]
        res_senti_label = response_content["sentiment_label"]
        res_senti_label_reason = str(response_content["sentiment_label_reason"])
        res_posi_score = response_content["positive_score"]
        res_nega_score = response_content["negative_score"]
        return {
            'statusCode': 200,
            "senti_label": res_senti_label,
            "senti_label_reason": res_senti_label_reason,
            "posi_score": res_posi_score,
            "nega_score": res_nega_score
            # 'body': json.dumps({"senti_label": res_senti_label,
            #                     "senti_label_reason": res_senti_label_reason,
            #                     "posi_score": res_posi_score,
            #                     "nega_score": res_nega_score})
            }
    except Exception as e:
        print("claude評価でエラーが発生しました。")
        return {
            'statusCode': 500,
            "senti_label": "claude error",
            "senti_label_reason": "claude error",
            "posi_score": "claude error",
            "nega_score": "claude error"
            # 'body': json.dumps({"senti_label": "claude error",
            #                     "senti_label_reason": "claude error",
            #                     "posi_score": "claude error",
            #                     "nega_score": "claude error"})
            }
