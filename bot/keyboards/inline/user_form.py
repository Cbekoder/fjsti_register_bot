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


def group_buttons(groups : list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(0, len(groups), 2):
        row = [
            InlineKeyboardButton(text=group, callback_data=f"group_{group}")
            for group in groups[i:i + 2]
        ]
        inline_keyboard.append(row)
    buttons = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return buttons


def profile_buttons(lang='uz') -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-lastname'),
                    callback_data='edit_lastname'
                ),
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-firstname'),
                    callback_data='edit_firstname'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-middlename'),
                    callback_data='edit_middlename'
                ),
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-level'),
                    callback_data='edit_level'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-faculty'),
                    callback_data='edit_faculty'
                ),
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-direction'),
                    callback_data='edit_direction'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-course'),
                    callback_data='edit_course'
                ),
                InlineKeyboardButton(
                    text=get_text(lang, 'edit-group'),
                    callback_data='edit_group'
                )
            ]
        ]
    )
    return buttons