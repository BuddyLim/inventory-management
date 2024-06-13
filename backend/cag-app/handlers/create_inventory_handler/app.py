import json
import boto3
import os
import uuid
from decimal import Decimal
from datetime import datetime


TABLE_NAME = os.environ['TABLE_NAME']
ENDPOINT_OVERRIDE = os.environ['ENDPOINT_OVERRIDE']


dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_OVERRIDE)
table = dynamodb.Table(TABLE_NAME)

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
    id = str(uuid.uuid4())
    last_updated_dt = datetime.now() 
    last_updated_str = last_updated_dt.strftime("%m/%d/%Y %H:%M:%S")
    print("---")
    print("Table name: ", TABLE_NAME)
    print("ID: ", id)
    print("last_updated_dt: ", last_updated_str)
    print("---")

    table.put_item(
        Item={
            'id': id,
            "name": "Notebook", 
            "category": "Stationary", 
            "price": Decimal(5.5),
            "last_updated_dt": last_updated_str 
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": id,
            "last_updated_dt": last_updated_str
            # "location": ip.text.replace("\n", "")
        }),
    }
