
from flask import Blueprint
from flask_restx import Api
from blueprints.endpoints.hello_world import namespace as hello_world_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')

api_extension = Api(
    blueprint,
    title='The API Demo',
    version='1.0',
    description='Application to demonstrate an API with DynamoDB',
    doc='/doc'
)

api_extension.add_namespace(hello_world_ns)