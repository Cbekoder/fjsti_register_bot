from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tuzilma.models import Level, Faculty, Direction
from data.scenario import get_text
from django.utils import translation
from loader import orm_async


async def level_buttons(lang='uz') -> InlineKeyboardMarkup:
    translation.activate(lang)
    levels = await orm_async(list, Level.objects.all())
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=level.name,
                    callback_data=f'level_{level.id}'
                )
            ] for level in levels
        ]
    )
    return buttons


async def faculty_buttons(lang='uz') -> InlineKeyboardMarkup:
    translation.activate(lang)
    faculties = await orm_async(list, Faculty.objects.filter(is_active=True))
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=faculty.name,
                    callback_data=f"faculty_{faculty.id}"
                ),
            ] for faculty in faculties if faculty.is_active
        ]
    )
    return buttons


async def direction_buttons(faculty_id, lang='uz') -> InlineKeyboardMarkup:
    translation.activate(lang)
    directions = await orm_async(list, Direction.objects.filter(faculty__id=faculty_id))
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=direction.name,
                    callback_data=f"direction_{direction.id}"
                ),
            ] for direction in directions
        ]
    )
    return buttons


def course_buttons(max_course) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{number}",
                    callback_data=f"course_{number}"
                ) for number in range(1, max_course + 1)
            ]
        ]
    )
    return buttons


def group_buttons(groups: list) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in range(0, len(groups), 2):
        row = [
            InlineKeyboardButton(text=group.name, callback_data=f"group_{group.id}")
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
