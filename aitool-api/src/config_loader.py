import os
import yaml
from typing import Dict
from utils.common_utils import default_config_update


def load_config(config_file_path: str) -> Dict:
    default_config = {
        'server': {
            'ip': '127.0.0.1',
            'port': 5000,
            'debug': True,
            'environment': 'dev',
        },
        'frontend': {
            'origin': 'http://127.0.0.1:8081',
        },
    }

    try:
        with open(config_file_path, 'r') as file:
            yaml_config = yaml.safe_load(file)
            if yaml_config:
                default_config.update(yaml_config)
    except FileNotFoundError:
        print('Config file not found, using defaults.')
    except yaml.YAMLError as e:
        print(f'Error parsing YAML, using defaults: {e}')

    return default_config


def load_gpt_api_config(config_file_path: str) -> Dict:
    default_config = {
        'api_key': '',
        'basic_url': 'https://genai.hkbu.edu.hk/general/rest',
        'model_name': 'gpt-4-o-mini',
        'api_version': '2024-05-01-preview',
    }

    try:
        with open(config_file_path, 'r') as file:
            yaml_config = yaml.safe_load(file)
            if yaml_config:
                default_config = default_config_update(default_config, yaml_config)
    except FileNotFoundError:
        print('Config file not found.')
    except yaml.YAMLError:
        print('Error parsing YAML.')

    return default_config


def update_env_config(server_config: Dict, gpt_api_config: Dict):
    env = {
        'ip': os.getenv('SERVER_IP'),
        'port': os.getenv('SERVER_PORT'),
        'debug': os.getenv('SERVER_DEBUG'),
        'api_key': os.getenv('API_KEY'),
    }
    if server_config is not None:
        if env['ip'] is not None:
            server_config['server']['ip'] = env['ip']
        if env['port'] is not None:
            server_config['server']['port'] = int(env['port'])
        if env['debug'] is not None:
            if env['debug'].lower() == 'true':
                server_config['server']['debug'] = True
            elif env['debug'].lower() == 'false':
                server_config['server']['debug'] = False
    if gpt_api_config is not None and env['api_key'] is not None:
        gpt_api_config['api_key'] = env['api_key']
