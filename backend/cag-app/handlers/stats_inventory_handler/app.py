import json
import boto3
import os
from typing import Dict, Tuple, List
from mypy_boto3_dynamodb import ServiceResource
from collections import Counter
from itertools import groupby
from decimal import Decimal

TABLE_NAME = os.environ['TABLE_NAME']
AWS_ENVIRON = os.environ.get('AWS_ENVIRON', 'AWS')
ENDPOINT_OVERRIDE = os.environ.get('ENDPOINT_OVERRIDE', None)
REGION = os.environ.get('REGION', 'us-east-1')

if AWS_ENVIRON == 'AWS_SAM_LOCAL':
    dynamodb: ServiceResource = boto3.resource('dynamodb', endpoint_url=ENDPOINT_OVERRIDE)
else: 
    dynamodb: ServiceResource = boto3.resource('dynamodb')

table = dynamodb.Table(TABLE_NAME)


class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


def counterize(x):
    return Counter({k : float(v) for k, v in x.iteritems()})


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
           "total_price": round(float(total_price), 2),
           "count": count,
           "category": key
        })

    return stats_list

def lambda_handler(event, context):
    evt_val = json.loads(event['body'])
    category = evt_val.get('category', 'all')

    print("Table name: ", TABLE_NAME)

    if(category == 'all'):
        item_list = table.scan()['Items']
    else:
        item_list = table.scan(
            FilterExpression=f'(#category IN (:category))',
            ExpressionAttributeNames={ "#category": "category" },
            ExpressionAttributeValues={ ":category" : category }
        )['Items']

    stats_list = aggregate_list(item_list=item_list)
     
    return {
        "statusCode": 200,
        "body": json.dumps({
            "items": stats_list,
        }, cls=DecimalEncoder),
    }
