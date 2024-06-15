import json
import boto3
import os
from typing import Dict, Tuple
from mypy_boto3_dynamodb import ServiceResource
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
      return float(obj)
    return json.JSONEncoder.default(self, obj)


def dt_query_builder(dt_dict: Dict) -> Tuple[str, Dict, Dict]:
    FilterExpression = '(#last_updated_dt BETWEEN :dt_from AND :dt_to)'
    ExpressionAttributeValues= {
        ':dt_from': dt_dict['dt_from'],
        ':dt_to': dt_dict['dt_to']
    }
    ExpressionAttributeNames= {
        '#last_updated_dt': 'last_updated_dt',
    }

    return ( FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues )


def query_items(dt_dict: Dict):
    ( FilterExpression, ExpressionAttributeNames, ExpressionAttributeValues ) = dt_query_builder(dt_dict=dt_dict)
    FilterExpression = FilterExpression
    ExpressionAttributeNames = ExpressionAttributeNames
    ExpressionAttributeValues = ExpressionAttributeValues

    item_list = table.scan(
        FilterExpression=FilterExpression,
        ExpressionAttributeNames=ExpressionAttributeNames,
        ExpressionAttributeValues=ExpressionAttributeValues
    )['Items']

    total_price = round(sum(float(item['price']) for item in item_list), 2)

    return {
       "items": item_list,
       "total_price": total_price
    }


def lambda_handler(event, context):
    print("Table name: ", TABLE_NAME)

    if(event['httpMethod'] == 'GET'):   
        item_list = table.scan()['Items']

        return {
            "statusCode": 200,
            "body": json.dumps({
                "items": item_list,
            }, cls=DecimalEncoder),
        }
    
    print(event)

    evt_val = json.loads(event['body'])
    filter_dict = evt_val.get('filters', {})

    if 'dt_range' not in filter_dict:
        item_list = table.scan()['Items']

        return {
            "statusCode": 200,
            "body": json.dumps({
                "items": item_list,
            }, cls=DecimalEncoder),
        }

    resp_dict = query_items(filter_dict['dt_range'])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*", # Required for CORS support to work
        },
        "body": json.dumps(resp_dict, cls=DecimalEncoder),
    }
