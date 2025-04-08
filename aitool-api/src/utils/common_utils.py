def is_empty(params):
    if params is None:
        return True
    else:
        if isinstance(params, str):
            return params.strip() == ''
    return False


def default_config_update(default_config, config_dict):
    for key in default_config.keys():
        config_key = key.replace('_', '-')
        if not is_empty(config_dict):
            default_config[key] = config_dict.get(config_key)
    return default_config


def get_llm_api_url(config):
    return ''.join([
        config['basic_url'],
        '/deployments/',
        config['model_name'],
        '/chat/completions/?api-version=',
        config['api_version'],
    ])


def get_llm_api_headers(config):
    return {
        'Content-Type': 'application/json',
        'api-key': config['api_key'],
    }


def success(data, code=200, message=''):
    return {
        'success': True,
        'code': code,
        'data': data,
        'message': message,
    }


def failure(code, message=''):
    return {
        'success': False,
        'code': code,
        'data': None,
        'message': message,
    }
