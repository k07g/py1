import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "books")
DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT")  # ローカル: http://localhost:8000


def get_table():
    kwargs = {}
    if DYNAMODB_ENDPOINT:
        kwargs = {
            "endpoint_url": DYNAMODB_ENDPOINT,
            "region_name": "us-east-1",
            "aws_access_key_id": "dummy",
            "aws_secret_access_key": "dummy",
        }
    dynamodb = boto3.resource("dynamodb", **kwargs)
    return dynamodb.Table(TABLE_NAME)


def put_book(item: dict) -> dict:
    table = get_table()
    table.put_item(Item=item)
    return item


def get_book(book_id: str) -> dict | None:
    table = get_table()
    response = table.get_item(Key={"id": book_id})
    return response.get("Item")


def update_book(book_id: str, updates: dict) -> dict | None:
    table = get_table()

    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates)
    expr_names = {f"#{k}": k for k in updates}
    expr_values = {f":{k}": v for k, v in updates.items()}

    try:
        response = table.update_item(
            Key={"id": book_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_NEW",
        )
        return response["Attributes"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return None
        raise


def delete_book(book_id: str) -> bool:
    table = get_table()
    try:
        table.delete_item(
            Key={"id": book_id},
            ConditionExpression="attribute_exists(id)",
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        raise


def list_books(limit: int = 20, last_key: str | None = None) -> tuple[list[dict], str | None]:
    table = get_table()
    kwargs = {"Limit": limit}
    if last_key:
        kwargs["ExclusiveStartKey"] = {"id": last_key}

    response = table.scan(**kwargs)
    next_key = response.get("LastEvaluatedKey", {}).get("id")
    return response.get("Items", []), next_key
