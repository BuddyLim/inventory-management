import json
import boto3
import os
from mypy_boto3_dynamodb import ServiceResource
from boto3.dynamodb.conditions import Attr

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

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    print("Table name: ", TABLE_NAME)
    # print("Table status: ", table.table_status)

    resp = table.scan(
        FilterExpression='#name = :name',
        ExpressionAttributeValues= {
          ":name": "Notebook" 
        },
        ExpressionAttributeNames={
            "#name": "name"
        }
    )

    print(resp["Items"])

    response = table.scan(
        Limit=2
    )
    print(response)
    data = response['Items']

    return {
        "statusCode": 200,
        "body": json.dumps({
            "items": data,
            # "location": ip.text.replace("\n", "")
        }, cls=DecimalEncoder),
    }
