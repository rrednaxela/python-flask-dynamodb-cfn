import json
import boto3
import time
import uuid
import os
from flask import Flask
from blueprints.endpoints import blueprint as endpoint



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

app = Flask(__name__)

#@app.route('/api/hello_world')
#def hello_world():
#    return 'Hello, World!'

app.config['RESTX_MASK_SWAGGER'] = False

app.register_blueprint(endpoint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)