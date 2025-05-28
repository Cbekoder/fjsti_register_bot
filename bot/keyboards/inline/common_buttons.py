from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.scenario import get_text

language_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🇺🇿 O'zbek",
                callback_data="language_uz"
            ),
            InlineKeyboardButton(
                text="🇺🇸 English",
                callback_data="language_en"
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="language_ru"
            )
        ],

    ]
)


def request_confirm_buttons(lang='uz') -> InlineKeyboardMarkup:
    confirm_buttons = get_text(lang, "confirm")[::-1]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=confirm_text, callback_data=confirm_text)
                for confirm_text in confirm_buttons
            ]
        ]
    )
    return keyboard