import requests

def submit_single_interaction(prompt, mode, max_words=200):
    """
    Handles a single interaction for expanding or summarizing text.

    Parameters:
    - prompt (str): The text to process.
    - mode (str): Either "expand" or "extract".
    - max_words (int): Maximum word count for the output.

    Returns:
    - str: The response from the AI API or an error message.
    """
    expand_instruction = "Expand the following text by adding more details and context to each point. No more than the required word count: "
    extract_instruction = "Summarize the following text by extracting its key points. No more than the required word count: "

    if mode == "expand":
        instruction = expand_instruction
    elif mode == "extract":
        instruction = extract_instruction
    else:
        return "Invalid mode. Please specify 'expand' or 'extract'."

    conversation = [{"role": "user", "content": f"{instruction}{max_words}\n{prompt}"}]
    url = f"{basicUrl}/deployments/{modelName}/chat/completions/?api-version={apiVersion}"
    headers = {'Content-Type': 'application/json', 'api-key': apiKey}
    payload = {'messages': conversation, 'temperature': 0.6}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
