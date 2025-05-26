from aiogram import F
from aiogram.types import Message
from keyboards.default.menu_keyboard import menu_buttons
from keyboards.inline.common_buttons import language_buttons
from keyboards.inline.user_form import profile_buttons

from main.models import Student

from data.scenario import get_text, get_handler_keys
from loader import dp, redis_cl, orm_async


@dp.message(F.text.in_(get_handler_keys("settings-buttons", 0)))
async def handle_settings_0(message: Message):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    student = await orm_async(Student.objects.get, telegram_id=user_id)
    response = f"{get_text(lang, 'edit-lastname')}: {student.last_name}\n" \
                f"{get_text(lang, 'edit-firstname')}: {student.first_name}\n" \
                f"{get_text(lang, 'edit-middlename')}: {student.middle_name}\n" \
                f"{get_text(lang, 'edit-level')}: {get_text(lang, 'levels')[student.level_key]}\n" \
                f"{get_text(lang, 'edit-faculty')}: {get_text(lang, 'faculties')[student.faculty_key]}\n" \
                f"{get_text(lang, 'edit-direction')}: {get_text(lang, 'directions')[student.direction_key]}\n" \
                f"{get_text(lang, 'edit-course')}: {student.course}\n" \
                f"{get_text(lang, 'edit-group')}: {student.group}\n\n" \
                f"{get_text(lang, 'ask-edit')}"
    await message.delete()
    await message.answer(response, reply_markup=profile_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("settings-buttons", 1)))
async def handle_settings_1(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "select-language"), reply_markup=language_buttons)


@dp.message(F.text.in_(get_handler_keys("settings-buttons", 2)))
async def handle_settings_2(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))
