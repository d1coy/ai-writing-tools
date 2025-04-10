import requests
from utils.common_utils import get_llm_api_url, get_llm_api_headers, success, failure


def text_with_style(user_input, style, config):
    style_prompts = {
        "professional": "Please write in a professional tone, using formal language and industry-specific terminology "
                        "where appropriate. Maintain objectivity and avoid colloquialisms.",
        "academic": "Adopt an academic writing style with citations where needed, precise terminology, and a logical "
                    "flow of arguments. Use passive voice where appropriate and maintain scholarly rigor.",
        "friendly": "Write in a warm, conversational tone as if speaking to a colleague. Use contractions, personal "
                    "pronouns, and informal language where appropriate to create approachable content.",
        "casual": "Use very casual, everyday language with colloquialisms, simple sentence structures, and "
                  "conversational markers. Imagine you're texting a close friend.",
        "business": "Adopt a concise, results-oriented business writing style with clear action items, professional "
                    "terminology, and direct communication. Prioritize clarity over flourish.",
        "creative": "Be imaginative and expressive, using vivid descriptions, unconventional phrasing, and literary "
                    "devices. Prioritize originality and artistic expression over strict formality.",
        "persuasive": "Use rhetorical devices, compelling arguments, and emotional appeals to persuade the reader. "
                      "Structure content to build toward convincing conclusions.",
        "journalistic": "Write in an inverted pyramid style, putting the most important information first. Maintain "
                        "neutrality while making the content engaging and newsworthy.",
        "poetic": "Employ rhythmic language, metaphors, and sensory imagery. Prioritize aesthetic quality and "
                  "emotional resonance over literal precision.",
        "storytelling": "Structure content as a narrative with characters, conflict, and resolution. Use descriptive "
                        "language to create mental images and emotional engagement.",
    }

    style_prompt = style_prompts.get(style, '')

    if not style_prompt:
        return failure(code=400, message='Error: Invalid style selected.')

    full_prompt = (f'Your task is to rewrite this text:\n'
                   f'{user_input}\n\n'
                   f'Rewrite the text based on the this style guideline:\n'
                   f'{style_prompt}')

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
