import json
import boto3
import time
import uuid
import os
from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus


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
table = dynamodb.Table('requests')


def put_request(message):    
    response = table.put_item(
       Item={
           'uuid': str(uuid.uuid4()),
            'timestamp': int(time.time()),
            'text': message
        }
    )
    return response

result = put_request("hello world from ec2")



namespace = Namespace('messages', 'Messages API endpoints')

Message_model = namespace.model('Message', {
    'uuid': fields.String(
        readonly=True,
        description='Message identifier'
    ),
    'timestamp': fields.int(
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

Message_example = {'uuid': '5949b02d-1375-4741-b7dd-24c67ff9bcf5', 'name': 'Hello World!'}

@namespace.route('')
class messages(Resource):
    '''Get messages list and create new messages'''

    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_list_with(Message_list_model)
    def get(self):
        '''List with all the messages'''
        Message_list = table.query()

        return {
            'messages': Message_list['Items'],
            'total_records': len(Message_list)
        }

    @namespace.response(400, 'Message with the given name already exists')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(Message_model)
    @namespace.marshal_with(Message_model, code=HTTPStatus.CREATED)
    def post(self):
        '''Create a new Message'''

        if request.json['text'] == '':
            namespace.abort(400, 'Message text is empty')
        
        response = put_request(request.json['text'])

        return response, 201

@namespace.route('/<String:Message_id>')
class Message(Resource):
    '''Read, update and delete a specific Message'''

    @namespace.response(404, 'Message not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_with(Message_model)
    def get(self, Message_id):
        '''Get Message_example information'''

        return Message_example

    @namespace.response(400, 'Message with the given name already exists')
    @namespace.response(404, 'Message not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(Message_model, validate=True)
    @namespace.marshal_with(Message_model)
    def put(self, Message_id):
        '''Update Message information'''

        if request.json['name'] == 'Message name':
            namespace.abort(400, 'Message with the given name already exists')

        return Message_example

    @namespace.response(204, 'Request Success (No Content)')
    @namespace.response(404, 'Message not found')
    @namespace.response(500, 'Internal Server error')
    def delete(self, Message_id):
        '''Delete a specific Message'''

        return '', 204