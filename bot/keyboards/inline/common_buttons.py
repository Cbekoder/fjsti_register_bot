from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
