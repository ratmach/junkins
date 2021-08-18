import os

from flask import Flask
import json

from config.Config import JunkinsConfig

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET', 'SUPER_SECRET_KEY')

configuration = JunkinsConfig(json.load(open(os.getenv('config', 'config.json'), 'r')))
configuration.registerEndpoints(app)


@app.route('/')
def index():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host=configuration.host, port=configuration.port)
