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
