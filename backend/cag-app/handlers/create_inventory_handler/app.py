import json
import boto3
import os
from hashlib import sha1
from decimal import Decimal, Context
from datetime import datetime, timezone
from mypy_boto3_dynamodb import ServiceResource

TABLE_NAME = os.environ['TABLE_NAME']
AWS_ENVIRON = os.environ.get('AWS_ENVIRON', 'AWS')
ENDPOINT_OVERRIDE = os.environ.get('ENDPOINT_OVERRIDE', None)

if AWS_ENVIRON == 'AWS_SAM_LOCAL':
    dynamodb: ServiceResource = boto3.resource('dynamodb', endpoint_url=ENDPOINT_OVERRIDE)
else: 
    dynamodb: ServiceResource = boto3.resource('dynamodb')

table = dynamodb.Table(TABLE_NAME)
ctx = Context(prec=2)


def return_sha1_hash(text: str) -> str:
    return sha1(text.lower().encode('utf-8')).hexdigest()


def lambda_handler(event, context):
    evt_val = json.loads(event['body'])
    
    name = evt_val['name']
    price = evt_val['price']
    category = evt_val['category']

    id = return_sha1_hash(text=name)
    
    last_updated_dt = datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None).isoformat()

    print("---")
    print("Event: ", event)
    print("Table name: ", TABLE_NAME)
    print("ID: ", id)
    print("last_updated_dt: ", last_updated_dt)
    print("---")

    resp = table.update_item(
        Key={
            'id': id
        },
        UpdateExpression='SET #price= :price, #last_updated_dt= :last_updated_dt, #category = :category, #name = :name',
        ConditionExpression='attribute_exists(id) OR attribute_not_exists (id)',
        ExpressionAttributeValues={
            ':price':  Decimal(str(price)),
            ':last_updated_dt': last_updated_dt,
            ":category": category,
            ":name": name
        },
        ExpressionAttributeNames={
            '#price': 'price',
            '#last_updated_dt': 'last_updated_dt',
            '#category': 'category',
            '#name': 'name',
        },
        ReturnValues='ALL_NEW'
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*", # Required for CORS support to work
            "Access-Control-Allow-Methods": "GET,POST"
        },
        "body": json.dumps({
            "id": id,
            "last_updated_dt": last_updated_dt
        }),
    }
