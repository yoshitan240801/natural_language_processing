import numpy as np
import PIL
import requests
import json
import gradio
import boto3
  

def to_lambda_using_claude(in_data_for_claude):
    request_data = json.dumps(obj={"in_text": in_data_for_claude})
    print(type(request_data))
    lambda_client = boto3.client("lambda")
    lambda_function_name = "Lambda_Name_To_Kick_Calling_Claude"
    response = lambda_client.invoke(FunctionName=lambda_function_name,
                                    Payload=request_data)
    print(type(response))
    print(response)
    response_payload = response["Payload"].read()
    print(type(response_payload))
    print(response_payload)
    response_payload = response_payload.decode()
    print(type(response_payload))
    print(response_payload)
    response_data = json.loads(s=response_payload)
    print(type(response_data))  # dict型
    print(response_data)
    output_eval = response_data["senti_label"]
    output_reason = response_data["senti_label_reason"]
    output_positive_score = response_data["posi_score"]
    output_negative_score = response_data["nega_score"]
    return output_eval, output_reason, output_positive_score, output_negative_score


with gradio.Blocks() as gradio_ui:
    with gradio.Row():
        with gradio.Column():
            None
        with gradio.Column():
            gradio.Markdown(value="# 文章の熱意をAIが評価するwebアプリ")
            gradio.Image(value=PIL.Image.open(fp="/workdir/data/Display_Image.jpg"), type="pil", height=200, width=200)
        with gradio.Column():
            None
    with gradio.Row():
        with gradio.Column():
            ui_text_input = gradio.Textbox(value="", type="text", lines=7, placeholder="熱意を知りたい文章を入力してちょ", label="入力データ")
            ui_button = gradio.Button(value="Claudeさん、熱意を調べて！")
    with gradio.Row():
        with gradio.Column():
            ui_text_output = gradio.Textbox(value="", type="text", lines=1, label="評価")
            ui_text_output_3 = gradio.Textbox(value="", type="text", lines=1, label="ポジティブスコア")
            ui_text_output_4 = gradio.Textbox(value="", type="text", lines=1, label="ネガティブスコア")
        with gradio.Column():
            ui_text_output_2 = gradio.Textbox(value="", type="text", lines=7, label="評価の理由")
    ui_button.click(fn=to_lambda_using_claude,
                    inputs=ui_text_input,
                    outputs=[ui_text_output, ui_text_output_2, ui_text_output_3, ui_text_output_4])


if __name__ == "__main__":
    # gradio_ui.launch()
    gradio_ui.launch(server_name="0.0.0.0", server_port=8080)  # http://127.0.0.1:8080でアクセス出来る
    # gradio_ui.launch(share=True, server_name="0.0.0.0")  # HuggingFace側でPublicアクセス出来るリンクを作る
