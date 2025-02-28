import requests
import os

gemini_api_key = os.getenv("gemini_api_key")
dir_path = os.path.join(os.path.abspath(os.curdir), 'config')

def send_message_to_ai(message_history, current_message, channel, username):
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': gemini_api_key,
    }
    with open(os.path.join(dir_path, "prompt.txt"), 'r', encoding='utf-8') as f:
        message_to_bot = f.read()
    message_to_bot = (message_to_bot
                      .replace("{message}", current_message)
                      .replace("{username}", username)
                      .replace("{chnl}", channel)
                      .replace('{history}', "\n".join([f"{i.username}: {i.message}" for i in message_history[-25:]])))

    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': message_to_bot,
                    },
                ],
            },
        ],
    }
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )
    response_message = response.json()['candidates'][0]['content']['parts'][0]['text'].replace('\n', " ")
    return response_message
