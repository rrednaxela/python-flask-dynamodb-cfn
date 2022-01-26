import boto3
import time
import uuid
import os
from flask import request
from flask_restx import Namespace, Resource, fields


# Get environment variables
access_key = os.getenv('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')
aws_region_name = os.environ.get('REGION_NAME')
table_name = os.environ.get('TABLE_NAME')

#connect dynamodb
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret,
    region_name=aws_region_name,
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(table_name)

#uuid helper
def is_valid_uuid(value):
    try:
        uuid.UUID(value)
 
        return True
    except ValueError:
        return False

#create message db method
def put_request(message):
    the_id = str(uuid.uuid4())
    timestamp = int(time.time())
    table.put_item(
       Item={
            'uuid': the_id,
            'timestamp': timestamp,
            'text': message
        }
    )
    return {'uuid': the_id, 'timestamp': timestamp, 'text': message}

#cerate a test message
result = put_request("hello world from ec2")



namespace = Namespace('messages', 'Messages API endpoints')

Message_model = namespace.model('Message', {
    'uuid': fields.String(
        readonly=True,
        description='Message identifier'
    ),
    'timestamp': fields.Integer(
        readonly=True,
        description='Message timestamp'
    ),
    'text': fields.String(
        required=True,
        description='Message text'
    )
})

Message_list_model = namespace.model('MessageList', {
    'messages': fields.Nested(
        Message_model,
        description='List of messages',
        as_list=True
    ),
    'total_records': fields.Integer(
        description='Total number of messages',
    ),
})

@namespace.route('')
class messages(Resource):
    '''Get messages list and create new messages'''

    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_list_with(Message_list_model)
    def get(self):
        '''List with all the messages'''
        try:
            query = table.scan()
            Message_list = query['Items']
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            namespace.abort(500, 'Internal Server error')

        return {
            'messages': Message_list,
            'total_records': len(Message_list)
        }

    @namespace.response(400, 'Message text is invalid or empty')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(Message_model)
    @namespace.marshal_with(Message_model, code=201)
    def post(self):
        '''Create a new Message'''

        if request.json['text'] == '':
            namespace.abort(400, 'Message text is empty')
        
        response = put_request(request.json['text'])

        return response, 201

@namespace.route('/<string:Message_id>')
class Message(Resource):
    '''Read or delete a specific Message'''

    @namespace.response(400, 'Invalid message uuid')
    @namespace.response(404, 'Message not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_with(Message_model)
    def get(self, Message_id):
        '''Get a single message by uuid'''

        if not is_valid_uuid(Message_id):
            namespace.abort(400, 'Invalid message uuid')

        try:
            query = table.get_item(
                Key={
                    'uuid': Message_id
                }
            )
        except Exception as err:
            namespace.abort(500, 'Internal Server error')
        else:
            if not 'Item' in query:
                namespace.abort(400, 'Message not found')
            else:
                Message = query['Item']
                return {
                    'uuid': Message['uuid'],
                    'timestamp': int(Message['timestamp']),
                    'text': Message['text']
                }, 200


    @namespace.response(204, 'Request Success (No Content)')
    @namespace.response(500, 'Internal Server error')
    def delete(self, Message_id):
        '''Delete a specific Message'''
        if not is_valid_uuid(Message_id):
            namespace.abort(400, 'Invalid message uuid')

        try:
            query = table.delete_item(
                Key={
                    'uuid': Message_id
                }
            )
        except Exception as err:
            namespace.abort(500, 'Internal Server error')
        else:
            return '', 204