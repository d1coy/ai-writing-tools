import requests
from utils.common_utils import get_llm_api_url, get_llm_api_headers, success, failure


def analyze_text_features(text, config):
    analyze_prompt = f"""
        Please analyze the main features of the following text, including:
        1. Language style characteristics
        2. Common vocabulary and sentence patterns
        3. Text structure characteristics
        4. Other significant features

        Text content (take the first 1000 words):
        {text[:1000]}

        Please summarize the features in concise language and directly output the analysis results:
    """

    conversation = [{'role': 'user', 'content': analyze_prompt}]

    url = get_llm_api_url(config)
    headers = get_llm_api_headers(config)
    payload = {'messages': conversation, 'temperature': 0.5}

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return success(data['choices'][0]['message']['content'])
    else:
        error_message = f'Error: {response.status_code}, {response.text}'
        return failure(code=response.status_code, message=error_message)


def rewrite(user_input, features, config):
    full_prompt = (f'Use the following features to rewrite the text:\n'
                   f'Features: {features}\n\n'
                   f'Text: {user_input}\n\n'
                   f'Output directly returns the modified text')

    conversation = [{'role': 'user', 'content': full_prompt}]

    url = get_llm_api_url(config)
    headers = get_llm_api_headers(config)
    payload = {'messages': conversation, 'temperature': 0.5}

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return success(data['choices'][0]['message']['content'])
    else:
        error_message = f'Error: {response.status_code}, {response.text}'
        return failure(code=response.status_code, message=error_message)
