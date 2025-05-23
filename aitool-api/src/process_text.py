import requests
from utils.common_utils import get_llm_api_url, get_llm_api_headers, success, failure


def submit_single_interaction(prompt, mode, max_words, config):
    """
    Handles a single interaction for expanding or summarizing text.

    Parameters:
    - prompt (str): The text to process.
    - mode (str): Either "expand" or "extract".
    - max_words (int): Maximum word count for the output.

    Returns:
    - str: The response from the AI API or an error message.
    """
    expand_instruction = ('Expand the following text by adding more details and context to each point. '
                          'No more than the required word count: ')
    extract_instruction = ('Summarize the following text by extracting its key points. '
                           'No more than the required word count: ')

    if mode == 'expand':
        instruction = expand_instruction
    elif mode == 'extract':
        instruction = extract_instruction
    else:
        return failure(code=400, message="Invalid mode. Please specify 'expand' or 'extract'.")

    conversation = [{'role': 'user', 'content': f'{instruction}{max_words}\n{prompt}'}]

    url = get_llm_api_url(config)
    headers = get_llm_api_headers(config)
    payload = {'messages': conversation, 'temperature': 0.6}

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return success(data['choices'][0]['message']['content'])
    else:
        error_message = f'Error: {response.status_code}, {response.text}'
        return failure(code=response.status_code, message=error_message)
