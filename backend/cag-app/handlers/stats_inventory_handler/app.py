import json
import boto3
import os
from typing import Dict, Tuple, List
from mypy_boto3_dynamodb import ServiceResource
from collections import Counter
from itertools import groupby

TABLE_NAME = os.environ['TABLE_NAME']
ENDPOINT_OVERRIDE = os.environ['ENDPOINT_OVERRIDE']

dynamodb: ServiceResource = boto3.resource('dynamodb', endpoint_url=ENDPOINT_OVERRIDE)
table = dynamodb.Table(TABLE_NAME)

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


def counterize(x):
    return Counter({k : float(v) for k, v in x.iteritems()})


def category_query_builder(category_list: List[str]) -> Tuple[str, Dict, Dict]:
    FilterExpression = "",
    ExpressionAttributeNames  = {}
    ExpressionAttributeValues = {}

    for i, v in enumerate(category_list):
        # ExpressionAttributeNames[f"#{v}{i}"] = "category"
        ExpressionAttributeValues[f":category{i}"] = v

    ExpressionAttributeNames['#category'] = 'category'
    FilterExpression = f"(#category IN ({', '.join(ExpressionAttributeValues.keys())}))"

    return ( FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues )


def key_func(k):
    return k['category']


def aggregate_list(item_list: List[Dict]) -> List[Dict]:
    item_list = sorted(item_list, key=key_func)

    stats_list = []

    # I love this time complexity!
    for key, value in groupby(item_list, key_func):
        total_price = 0
        count = 0
        for d in value:
            count += 1
            total_price += d['price']

        stats_list.append({
           "total_price": total_price,
           "count": count,
           "category": key
        })

    return stats_list

def lambda_handler(event, context):
    evt_val = json.loads(event['body'])
    category_list = evt_val['category']

    print("Table name: ", TABLE_NAME)

    ( FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues ) = category_query_builder(category_list)

    item_list = table.scan(
        FilterExpression=FilterExpression,
        ExpressionAttributeNames=ExpressionAttributeNames,
        ExpressionAttributeValues=ExpressionAttributeValues
    )['Items']

    stats_list = aggregate_list(item_list=item_list)
     
    return {
        "statusCode": 200,
        "body": json.dumps({
            "items": stats_list,
        }, cls=DecimalEncoder),
    }
