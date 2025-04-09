import requests

def summarize_text_once(prompt):

    system_prompt = (
        "You cannot chat with user, just do: Summarize the main content of the text, "
        "ensure that the information is clear and easy to understand, and the total number of words cannot exceed 160. "
        "If the content is less than 30 words, just return 'Text is too short, please input the valid content.'"
    )

    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    url = f"{basicUrl}/deployments/{modelName}/chat/completions/?api-version={apiVersion}"
    headers = {'Content-Type': 'application/json', 'api-key': apiKey}
    payload = {'messages': conversation, 'temperature': 0.6}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"
