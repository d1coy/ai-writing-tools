from utils.common_utils import get_llm_api_url, get_llm_api_headers, success, failure
import requests


def translate(content, target_lang, config):
    system_prompt = f"""
        You are a translator.
        You need to translate the user's input content to the target language.
        The target language is {target_lang}.
        If you do not know the target language,
        you will response \"The target language is unknown.\".
    """

    conversation = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': content},
    ]

    url = get_llm_api_url(config)
    headers = get_llm_api_headers(config)
    payload = {'messages': conversation, 'temperature': 0.1}

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return success(data['choices'][0]['message']['content'])
    else:
        error_message = f'Error: {response.status_code}, {response.text}'
        return failure(code=response.status_code, message=error_message)
