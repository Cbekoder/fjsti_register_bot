from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.scenario import get_text


def phone_request_keyboard(lang='uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(lang, 'phone'), request_contact=True)]
        ],
        resize_keyboard=True
    )


def request_continue_buttons(lang='uz') -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(lang, "continue")),
            ],
            [
                KeyboardButton(text=get_text(lang, "cancel")),
            ]
        ],
        resize_keyboard=True,
    )
    return buttons


def request_cancel_button(lang='uz') -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(lang, "cancel")),
            ]
        ],
        resize_keyboard=True,
    )
    return buttons


def request_confirm_buttons(lang='uz') -> ReplyKeyboardMarkup:
    confirm_buttons = get_text(lang, "confirm")
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=confirm_text),
            ]
            for confirm_text in confirm_buttons
        ],
        resize_keyboard=True,
    )
    return buttons


def weekday_buttons(lang='uz'):
    weekdays = get_text(lang, "weekdays")

    keyboard = [[KeyboardButton(text=get_text(lang, "today"))]]
    for i in range(0, len(weekdays), 2):
        row = [KeyboardButton(text=day) for day in weekdays[i:i + 2]]
        keyboard.append(row)
    keyboard.append([KeyboardButton(text=get_text(lang, "cancel"))])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
