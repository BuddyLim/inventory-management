import json
import boto3
import os
from hashlib import sha1
from decimal import Context
from mypy_boto3_dynamodb import ServiceResource

TABLE_NAME = os.environ["TABLE_NAME"]
AWS_ENVIRON = os.environ.get("AWS_ENVIRON", "AWS")
ENDPOINT_OVERRIDE = os.environ.get("ENDPOINT_OVERRIDE", None)

if AWS_ENVIRON == "AWS_SAM_LOCAL":
    dynamodb: ServiceResource = boto3.resource(
        "dynamodb", endpoint_url=ENDPOINT_OVERRIDE
    )
else:
    dynamodb: ServiceResource = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)
ctx = Context(prec=2)


def return_sha1_hash(text: str) -> str:
    return sha1(text.lower().encode("utf-8")).hexdigest()


def lambda_handler(event, context):
    evt_val = json.loads(event["body"])

    id = evt_val["id"]

    print("---")
    print("Event: ", event)
    print("Table name: ", TABLE_NAME)
    print("ID: ", id)
    print("---")

    resp = table.delete_item(Key={"id": id})

    status_code = resp["ResponseMetadata"]["HTTPStatusCode"]

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            "Access-Control-Allow-Methods": "GET,POST",
        },
    }
