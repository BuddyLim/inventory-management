import json
import boto3
import os
from typing import Dict
from hashlib import sha1
from decimal import Decimal
from datetime import datetime
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import ServiceResource


TABLE_NAME = os.environ['TABLE_NAME']
ENDPOINT_OVERRIDE = os.environ['ENDPOINT_OVERRIDE']


dynamodb: ServiceResource = boto3.resource('dynamodb', endpoint_url=ENDPOINT_OVERRIDE)
table = dynamodb.Table(TABLE_NAME)


def return_sha1_hash(text: str) -> str:
    return sha1(text.encode('utf-8')).hexdigest()


def lambda_handler(event, context):
    evt_val = json.loads(event['body'])
    
    name = evt_val['name']
    price = evt_val['price']
    category = evt_val['category']

    id = return_sha1_hash(text=name)
    
    last_updated_dt = datetime.now() 
    last_updated_str = last_updated_dt.strftime("%m/%d/%Y %H:%M:%S")

    print("---")
    print("Event: ", event)
    print("Table name: ", TABLE_NAME)
    print("ID: ", id)
    print("last_updated_dt: ", last_updated_str)
    print("---")

    resp = table.update_item(
        Key={
            'id': id
        },
        UpdateExpression='SET #price= :price, #last_updated_dt= :last_updated_dt, #category = :category, #name = :name',
        ConditionExpression='attribute_exists(id) OR attribute_not_exists (id)',
        ExpressionAttributeValues={
            ':price':  Decimal(price),
            ':last_updated_dt': last_updated_str,
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
        "body": json.dumps({
            "id": id,
            "last_updated_dt": last_updated_str
        }),
    }
