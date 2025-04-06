import yaml
from typing import Dict


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
