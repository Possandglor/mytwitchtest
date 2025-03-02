import os
from google import genai

from utils.singleton import SingletonMeta


class GenAI(metaclass=SingletonMeta):
    def __init__(self):
        self.genai_client = genai.Client(api_key=os.getenv("gemini_api_key"))
        self.dir_path = os.path.join(os.path.abspath(os.curdir), 'config')

    def send_message_to_ai(self,message_history, current_message, channel, username):
        with open(os.path.join(self.dir_path, "prompt.txt"), 'r', encoding='utf-8') as f:
            message_to_bot = f.read()
        message_to_bot = (message_to_bot
                          .replace("{message}", current_message)
                          .replace("{username}", username)
                          .replace("{chnl}", channel)
                          .replace('{history}',
                                   "\n".join([f"{i.username}: {i.message}" for i in message_history[-25:]])))

        response = self.genai_client.models.generate_content(
        model="gemini-1.5-flash-8b",
        contents=message_to_bot,
        )
        return response.text