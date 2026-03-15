"""ローカル DynamoDB にテーブルを作成するスクリプト"""
import boto3
from botocore.exceptions import ClientError

ENDPOINT = "http://localhost:8000"
TABLE_NAME = "books"

dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

try:
    dynamodb.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        BillingMode="PAY_PER_REQUEST",
    )
    print(f"テーブル '{TABLE_NAME}' を作成しました")
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceInUseException":
        print(f"テーブル '{TABLE_NAME}' は既に存在します")
    else:
        raise
