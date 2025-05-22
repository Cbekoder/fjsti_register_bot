import json
import urllib.parse
import requests
from pathlib import Path

from core.settings import env, BASE_DIR

file_path = BASE_DIR.parent / "files/scenario.json"

with open(file_path, "r", encoding="utf-8") as file:
    texts = json.load(file)

def get_text(lang: str = "uz", key: str = None):
    if lang not in texts.keys():
        lang = "uz"
    if key is not None:
        try:
            return texts[lang][key]
        except KeyError:
            pass
    return texts[lang]

class TelegramService:
    def __init__(self):
        self.bot_token = env.str('BOT_TOKEN')

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        try:
            prev_params = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }

            response = requests.post(
                url=url,
                params=prev_params,
            )
            return response.json()
        except Exception as e:
            print(e)
            return None

    def send_file(self, chat_id, file_path, caption=None):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"

        try:
            with open(file_path, 'rb') as file:
                data = {
                    "chat_id": chat_id,
                    "caption": caption,
                    "parse_mode": "HTML",
                }
                files = {
                    "document": file,
                }
                response = requests.post(
                    url=url,
                    data=data,
                    files=files,
                )
                return response.json()
        except Exception as e:
            print(e)
            return None

Telegram = TelegramService()
