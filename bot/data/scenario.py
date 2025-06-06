from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent.parent / "files/scenario.json"

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


def get_handler_keys(key: str, index: int = None) -> list:
    languages = ['uz', 'ru', 'en']
    if index is not None:
        return [get_text(lang, key)[index] for lang in languages]
    return [get_text(lang, key) for lang in languages]
