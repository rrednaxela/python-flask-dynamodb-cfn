# python-flask-dynamodb-cfn
## What is this?
A demo message API application written in Python, using flask. The application uses a dynamoDB database as backend for storing messages. It can be deployed on AWS using a cloudformation template, also contained in this repository.

## Getting started
* You need an AWS account and an access key / access secret for a user who can read/write from DynamoDB tables.
* Create the cloudformation stack using the template cf-theapp-with-vpc.json
* After the delpoyment is complete, the UI can be found at http://<hostname/IP>/api/doc - the full link can be found in the stack Outputs
* The UI contains more information on the API capabilities

## About the clouformation template
By creating a stack using the cf-theapp-with-vpc.json template, you should get
* a VPC with an internet gateway
* a dynamoDB table
* an EC2 instance where the python app is pulled from this repository and then started

## Todo
The scope of this demo is to provide a complete running solution. Feel free to contribute to the todos below or add your own ideas.
* Run the app with a dedicated user behind an apache or nginx proxy
* upgrade the Amazon Linux image to a current version
* Implement API authorization
* Add https using letsencrypt
* Add a nice html message board / chat UI 

## Credits
* The python app was inspired by https://www.imaginarycloud.com/blog/flask-python/
* The cloudformation template is based on the AWS sample template "WordPress basic single instance" from https://s3.eu-west-2.amazonaws.com/cloudformation-templates-eu-west-2/WordPress_Single_Instance.template
