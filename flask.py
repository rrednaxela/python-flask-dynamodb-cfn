import json
import boto3
import time
import uuid
import os


# Get environment variables
access_key = os.getenv('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')

#connect dynamodb
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret,
    region_name="eu-west-3",
)
dynamodb = session.resource('dynamodb')

def put_request(message):

    # dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")

    table = dynamodb.Table('requests')
    response = table.put_item(
       Item={
           'uuid': str(uuid.uuid4()),
            'timestamp': int(time.time()),
            'message': message
        }
    )
    return response

result = put_request("hello world from ec2")

print(json.dumps(result))