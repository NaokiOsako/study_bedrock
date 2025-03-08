import boto3
import json
from decimal import Decimal


session = boto3.Session(profile_name='osako')

# Bedrock クライアントの作成
bedrock_runtime_client = session.client(service_name='bedrock-runtime')

# 宣言
input_text = "どんな会社?"

model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
content_type = 'application/json'
accept = 'application/json'
body = json.dumps(
    {   
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{
            "role": "user",
            "content": input_text
        }]    
    }
)


# APIリクエスト
response = bedrock_runtime_client.invoke_model(body=body, modelId=model_id, contentType=content_type, accept=accept)

# 料金
input_token_count = Decimal(response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-input-token-count'])
output_token_count = Decimal(response['ResponseMetadata']['HTTPHeaders']['x-amzn-bedrock-output-token-count'])
cost = (Decimal(0.00000025) * input_token_count + Decimal(0.00000125) * output_token_count) * 150
print(f"Input Token Count: {input_token_count}")
print(f"Output Token Count: {output_token_count}")
print(f"cost: {cost.quantize(Decimal('0.001'))}円")

# レスポンスの処理
response_body = json.loads(response.get('body').read().decode('utf-8'))
answer = response_body['content'][0]['text']
print(answer)
