import boto3


def call_amazon_nova_using_bedrock(input_text_data):
    boto3_client = boto3.client("bedrock-runtime",
                                region_name="ap-northeast-1")
    model_id = "MODEL ID"  # amazon nova pro
    SYSTEM_PROMPT = """
    与えられたテキストはコンタクトセンターの通話を記録したもので、CUはお客様を表し、OPはオペレータの発言になります。
    この通話が下記のA.～B.の特徴のいずれかに当てはまる場合はYes、いずれにも当てはまらない場合はNoを出力してください。
    A. お客様が不在で留守番電話に繋がったもの
    B. 担当のオペレータが不在だったもの
    """
    USER_PROMPT = input_text_data
    prompt = """
    {a}
    <text>
    {b}
    </text>
    """.format(a=SYSTEM_PROMPT, b=USER_PROMPT)
    amazon_nova_input_with_prompt = [{"role": "user",
                                      "content": [{"text": prompt}]}]
    amazon_nova_response = boto3_client.converse(modelId=model_id,
                                                 messages=amazon_nova_input_with_prompt,
                                                 inferenceConfig={"temperature": 0.2})
    amazon_nova_response_text = amazon_nova_response["output"]["message"]["content"][0]["text"]
    return amazon_nova_response_text