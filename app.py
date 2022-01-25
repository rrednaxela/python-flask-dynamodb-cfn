from flask import Flask
from blueprints.endpoints import blueprint as endpoint


app = Flask(__name__)

#@app.route('/api/hello_world')
#def hello_world():
#    return 'Hello, World!'

app.config['RESTX_MASK_SWAGGER'] = False

app.register_blueprint(endpoint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)