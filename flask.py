import json
import boto3
import time
import uuid
import os
from flask import Flask


# Get environment variables
access_key = os.getenv('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')
aws_region_name = os.environ.get('REGION_NAME')

#connect dynamodb
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret,
    region_name=aws_region_name,
)
dynamodb = session.resource('dynamodb')

def put_request(message):

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

app = Flask(__name__)

@app.route('/api/hello_world')
def hello_world():
    return 'Hello, World!'