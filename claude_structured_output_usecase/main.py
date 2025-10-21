import csv
import datetime
import dotenv
import os
import time

import boto3
import pandas as pd


dotenv.load_dotenv()
CLAUDE_MODEL_ID = os.getenv("BEDROCK_CLAUDE_3_5_MODEL_ID")  # Claude 3.5 Sonnet
CLAUDE_CLIENT = boto3.client("bedrock-runtime",
                             region_name="ap-northeast-1")
FUNCTION_CALLING_DESCRIPTION = (
    "あなたはコンタクトセンターで音声通話テキストからお客様のニーズ(VOC)を把握する業務を10年以上行っている専門家です。\n"
    "与えられたテキストは過去の通話を記録したもので、CUはお客様を表し、OPはオペレータの発言になります。"
)
INPUT_DATA_PATH = "./conversation_text.csv"

# ポジティブ/ニュートラル/ネガティブ判定ツール用
FUNCTION_CALLING_NAME_a = "emotion_judge"

NAME_1_IN_FUNCTION_CALLING_a = "predict_customer_emotion_by_LLM"
PROMPT_1_IN_FUNCTION_CALLING_a = (
    "会話はコンタクトセンターでの電話のやりとりです。\n"
    "この会話全体を通して、お客様の感情をポジティブかニュートラルかネガティブかを判定してください。"
)

# VOC/CRおよび構造化データ出力ツール用
FUNCTION_CALLING_NAME_b = "VOC_CR_judge"

NAME_1_IN_FUNCTION_CALLING_b = "extract_customer_request_by_LLM"
PROMPT_1_IN_FUNCTION_CALLING_b = (
    "会話はコンタクトセンターでの電話のやりとりです。\n"
    "この会話全体を踏まえて、お客様(CU)のVOCもしくはコンタクトリーズン(CR)を抽出してください。\n"
    "また、以下の指示を守ってください。\n\n"
    "# 指示\n"
    "- 出力はリスト形式にしてください。\n"
    "- VOCもしくはCRが複数含まれている場合は、複数抽出してください。\n"
    "- VOCとCRは以下の定義を参考にしてください。\n\n"
    "# 定義\n"
    "特徴項目\tCR\tVOC\n"
    "目的\t特定のタスク完了、情報取得、問題解決\t感情・意見の表明、背景説明、将来的な改善要求\n"
    "性質\t客観的な事実、行動、要求\t主観的な意見、感情、評価、要望、期待\n"
    "問い\tWhat(何をしたか、何を求めたか)\tWhy,How(なぜそう感じたか、どのように感じたか)\n"
    "具体例\t「注文内容を変更したい」\t「注文後の変更手続きがサイト上でできないのは不便だ」\n\n"
)

NAME_2_IN_FUNCTION_CALLING_b = "predict_VOC_or_CR_by_LLM"
PROMPT_2_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したものがVOCかCRかを出力してください。\n"
    "抽出したもの毎にリストで出力してください。"
).format(a=NAME_1_IN_FUNCTION_CALLING_b)

NAME_3_IN_FUNCTION_CALLING_b = "predict_category_by_LLM"
PROMPT_3_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、以下の定義を踏まえて当てはまるカテゴリを、1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 定義\n"
    "カテゴリ\t具体的な内容\n"
    "手続きの問題（新規）\t申し込み手順の複雑さ、必要書類の多さなど\n"
    "手続きの問題（変更）\tプラン変更、変更手続きの煩雑さなど\n"
    "手続きの問題（解約）\t解約方法の分かりにくさ、必要以上に強引な引き止めなど\n"
    "工事・設置の問題\t希望日に予約が取れない、期間が長い、作業品質、作業員の態度が悪いなど\n"
    "料金・請求の問題\t想定外の料金、請求内容の分かりにくさ、支払い方法の不便さなど\n"
).format(a=NAME_1_IN_FUNCTION_CALLING_b)

NAME_4_IN_FUNCTION_CALLING_b = "suggest_target_by_LLM"
PROMPT_4_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、お客様が言及している対象を具体的なサービス名や手続き内容を、1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 出力例\n"
    "キャッシュバックのキャンペーン"
).format(a=NAME_1_IN_FUNCTION_CALLING_b)

NAME_5_IN_FUNCTION_CALLING_b = "suggest_happen_by_LLM"
PROMPT_5_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、{b}の対象に対して何が起きているのか、または何が起きていないのかの事実もしくは現象を、1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 出力例\n"
    "キャンペーンの申込が出来ない"
).format(a=NAME_1_IN_FUNCTION_CALLING_b, b=NAME_4_IN_FUNCTION_CALLING_b)

NAME_6_IN_FUNCTION_CALLING_b = "predict_evaluation_by_LLM"
PROMPT_6_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、お客様は{b}の事象に遭遇してどのような主観的な評価や感情を表しているか、1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 出力例\n"
    "キャッシュバックを申し込めないことに落胆を示している"
).format(a=NAME_1_IN_FUNCTION_CALLING_b, b=NAME_5_IN_FUNCTION_CALLING_b)

NAME_7_IN_FUNCTION_CALLING_b = "predict_reason_by_LLM"
PROMPT_7_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、お客様が{b}を表している理由を、経緯や背景を踏まえて1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 出力例\n"
    "契約時の担当者からキャッシュバックキャンペーンの話を聞いた時に「簡単に申し込める」と聞いていたため"
).format(a=NAME_1_IN_FUNCTION_CALLING_b, b=NAME_6_IN_FUNCTION_CALLING_b)

NAME_8_IN_FUNCTION_CALLING_b = "predict_expectation_by_LLM"
PROMPT_8_IN_FUNCTION_CALLING_b = (
    "{a}で抽出したもの毎に、お客様はどのようになってほしいと思っているか、その具体的な解決策を1つだけ出力してください。\n"
    "抽出したもの毎にリストで出力してください。\n\n"
    "# 出力例\n"
    "キャッシュバックキャンペーンの説明を行う時は安易な説明に留めず、申し込む時の方法を具体的に丁寧に説明するようにする"
).format(a=NAME_1_IN_FUNCTION_CALLING_b)


def structured_output_posi_nega_judge_tool():
    return {"toolSpec": {"name": FUNCTION_CALLING_NAME_a,
                         "description": FUNCTION_CALLING_DESCRIPTION,
                         "inputSchema": {"json": {"type": "object",
                                                  "properties": {NAME_1_IN_FUNCTION_CALLING_a: {"type": "string",
                                                                                                "enum": ["positive", "neutral", "negative"],
                                                                                                "description": PROMPT_1_IN_FUNCTION_CALLING_a}
                                                                },
                                                  "required": [NAME_1_IN_FUNCTION_CALLING_a]
                                                 }
                                        }
                        }
           }


def structured_output_VOC_CC_judge_tool():
    return {"toolSpec": {"name": FUNCTION_CALLING_NAME_b,
                         "description": FUNCTION_CALLING_DESCRIPTION,
                         "inputSchema": {"json": {"type": "object",
                                                  "properties": {NAME_1_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_1_IN_FUNCTION_CALLING_b},
                                                                 NAME_2_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "enum": ["VOC", "CR"],
                                                                                                "description": PROMPT_2_IN_FUNCTION_CALLING_b},
                                                                 NAME_3_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "enum": ["手続きの問題（新規）",
                                                                                                         "手続きの問題（変更）",
                                                                                                         "手続きの問題（解約）",
                                                                                                         "工事・設置の問題",
                                                                                                         "料金・請求の問題"],
                                                                                                "description": PROMPT_3_IN_FUNCTION_CALLING_b},
                                                                 NAME_4_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_4_IN_FUNCTION_CALLING_b},
                                                                 NAME_5_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_5_IN_FUNCTION_CALLING_b},
                                                                 NAME_6_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_6_IN_FUNCTION_CALLING_b},
                                                                 NAME_7_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_7_IN_FUNCTION_CALLING_b},
                                                                 NAME_8_IN_FUNCTION_CALLING_b: {"type": "array",
                                                                                                "items": {"type": "string"},
                                                                                                "description": PROMPT_8_IN_FUNCTION_CALLING_b}
                                                                },
                                                  "required": [NAME_1_IN_FUNCTION_CALLING_b,
                                                               NAME_2_IN_FUNCTION_CALLING_b,
                                                               NAME_3_IN_FUNCTION_CALLING_b,
                                                               NAME_4_IN_FUNCTION_CALLING_b,
                                                               NAME_5_IN_FUNCTION_CALLING_b,
                                                               NAME_6_IN_FUNCTION_CALLING_b,
                                                               NAME_7_IN_FUNCTION_CALLING_b,
                                                               NAME_8_IN_FUNCTION_CALLING_b]
                                                 }
                                        }
                        }
           }


def process_claude_with_function_calling(call_text_and_speaker, mcp_tool_function, mcp_tool_name):
    prompt = """
    <text>
    {a}
    </text>
    """.format(a=call_text_and_speaker)
    claude_input_with_prompt = [{"role": "user",
                                 "content": [{"text": prompt}]
                                }]
    claude_response = CLAUDE_CLIENT.converse(modelId=CLAUDE_MODEL_ID,
                                             messages=claude_input_with_prompt,
                                             inferenceConfig={"temperature": 0.2},
                                             toolConfig={"tools": [mcp_tool_function],
                                                         "toolChoice": {"tool": {"name": mcp_tool_name}}
                                                        })
    result = claude_response["output"]["message"]["content"][0]["toolUse"]["input"]
    return result


def read_csv_file_and_posi_nega_judge(csv_file_path):
    df = pd.DataFrame()
    with open(file=csv_file_path, mode="r", encoding="utf-8") as csvfile:
        csvfile_data_reader = csv.reader(csvfile)
        next(csvfile_data_reader, None)  # 1行目のヘッダーをスキップする
        print(datetime.datetime.now())
        i = 0
        for row in csvfile_data_reader:
            print(i)
            i += 1
            if row:
                result = process_claude_with_function_calling(call_text_and_speaker=row[1],
                                                              mcp_tool_function=structured_output_posi_nega_judge_tool(),
                                                              mcp_tool_name=FUNCTION_CALLING_NAME_a)
                dict_for_dataframe = {"asrID": row[0],
                                      "comment": row[1],
                                      "customer_emotion": result[NAME_1_IN_FUNCTION_CALLING_a]}
                time.sleep(1.5)
                try:
                    temp_df = pd.DataFrame(data=dict_for_dataframe,
                                           index=[0])  # 引数dataの辞書型データの値がスカラーなので引数indexで行数(行番号)を明示的に指定
                except Exception as e:
                    print(e, i, sep="：")
                    continue
                df = pd.concat(objs=[df, temp_df],
                               axis=0)
            else:
                continue
    print(datetime.datetime.now())
    return df


def read_df_and_VOC_CC_judge(negative_df):
    df = pd.DataFrame()
    print(datetime.datetime.now())
    for i, row in negative_df.iterrows():
        print(i)
        asr_id = row["asrID"]
        negative_comment = row["comment"]
        result = process_claude_with_function_calling(call_text_and_speaker=negative_comment,
                                                      mcp_tool_function=structured_output_VOC_CC_judge_tool(),
                                                      mcp_tool_name=FUNCTION_CALLING_NAME_b)
        dict_for_dataframe = {"asr_id": asr_id,
                              "negative_comment": negative_comment,
                              "extracted_comment": result[NAME_1_IN_FUNCTION_CALLING_b],
                              "VOC_CR": result[NAME_2_IN_FUNCTION_CALLING_b],
                              "VOC_CR_category": result[NAME_3_IN_FUNCTION_CALLING_b],
                              "VOC_CR_target": result[NAME_4_IN_FUNCTION_CALLING_b],
                              "VOC_CR_happen": result[NAME_5_IN_FUNCTION_CALLING_b],
                              "VOC_CR_evaluation": result[NAME_6_IN_FUNCTION_CALLING_b],
                              "VOC_CR_reason": result[NAME_7_IN_FUNCTION_CALLING_b],
                              "VOC_CR_expectation": result[NAME_8_IN_FUNCTION_CALLING_b]}
        time.sleep(3)
        try:
            temp_df = pd.DataFrame(data=dict_for_dataframe)
            temp_df = temp_df.explode(["extracted_comment",
                                       "VOC_CR",
                                       "VOC_CR_category",
                                       "VOC_CR_target",
                                       "VOC_CR_happen",
                                       "VOC_CR_evaluation",
                                       "VOC_CR_reason",
                                       "VOC_CR_expectation"])
        except Exception as e:
            print(e, i, sep="：")
            continue
        df = pd.concat(objs=[df, temp_df],
                       axis=0)
    print(datetime.datetime.now())
    return df


df_1 = read_csv_file_and_posi_nega_judge(csv_file_path=INPUT_DATA_PATH)
df_1_negative = df_1.query(expr="customer_emotion == 'negative'")
df_2 = read_df_and_VOC_CC_judge(negative_df=df_1_negative)
df_2_VOC = df_2.query(expr="VOC_CR == 'VOC'")
df_2_CR = df_2.query(expr="VOC_CR == 'CR'")
