from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data.scenario import get_text

def menu_buttons(lang='uz') -> ReplyKeyboardMarkup:
    menu_texts = get_text(lang, "menu-buttons")
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=menu_text),
            ]
            for menu_text in menu_texts
        ],
        resize_keyboard=True,
    )
    return buttons

def academic_menu_buttons(lang='uz') -> ReplyKeyboardMarkup:
    academic_texts = get_text(lang, "academic-buttons")
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=academic_text),
            ]
            for academic_text in academic_texts
        ],
        resize_keyboard=True,
    )
    return buttons

def hemis_menu_buttons(lang='uz') -> ReplyKeyboardMarkup:
    academic_texts = get_text(lang, "hemis-buttons")
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=academic_text),
            ]
            for academic_text in academic_texts
        ],
        resize_keyboard=True,
    )
    return buttons


def settings_buttons(lang='uz') -> ReplyKeyboardMarkup:
    settings_texts = get_text(lang, "settings-buttons")
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=settings_text),
            ]
            for settings_text in settings_texts
        ],
        resize_keyboard=True,
    )
    return buttons