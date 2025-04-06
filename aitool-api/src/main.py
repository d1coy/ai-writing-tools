import os
from flask import Flask
from flask_cors import CORS
from config_loader import load_config

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'hi'


if __name__ == '__main__':
    config_dir = os.path.join('..', 'config')
    config_file_name = 'config_server_dev.yaml'
    config_file_path = os.path.join(config_dir, config_file_name)
    config = load_config(config_file_path)
    if config:
        app.run(host=config['server']['ip'],
                port=config['server']['port'],
                debug=config['server']['debug'],
                )
    else:
        app.run(host='127.0.0.1', port=5000, debug=True)
