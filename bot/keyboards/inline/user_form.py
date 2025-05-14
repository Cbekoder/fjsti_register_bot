from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.scenario import get_text


def level_buttons(lang='uz') -> InlineKeyboardMarkup:
    levels = get_text(lang, 'levels')
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=level,
                    callback_data=f'level_{key}'
                )
            ] for key, level in levels.items()
        ]
    )
    return buttons


def faculty_buttons(lang='uz') -> InlineKeyboardMarkup:
    faculties = get_text(lang, 'faculties')
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=faculty,
                    callback_data=f"faculty_{key}"
                ),
            ] for key, faculty in faculties.items()
        ]
    )
    return buttons


def direction_buttons(lang='uz') -> InlineKeyboardMarkup:
    directions = get_text(lang, 'directions')
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=direction,
                    callback_data=f"direction_{key}"
                ),
            ] for key, direction in directions.items()
        ]
    )
    return buttons


def course_buttons() -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{number}",
                    callback_data=f"course_{number}"
                ) for number in range(1, 7)
            ]
        ]
    )
    return buttons


def group_buttons() -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{number}",
                    callback_data=f"group_{number}"
                ) for number in range(1, 5)
            ]
        ]
    )
    return buttons