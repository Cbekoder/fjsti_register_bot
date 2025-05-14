from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.user_form import faculty_buttons, direction_buttons, course_buttons, group_buttons
from states.user_form import UserForm
from data.scenario import get_text
from loader import dp, redis_cl, orm_async

from main.models import Student


@dp.callback_query(UserForm.level, F.data.startswith("level"))
async def process_level(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    level_key = callback_query.data.split("_")[1]
    await state.update_data(level=level_key)
    await callback_query.answer(f"You selected {level_key} faculty.")
    await callback_query.message.edit_text(get_text(lang, "enter-faculty"), reply_markup=faculty_buttons(lang))
    await state.set_state(UserForm.faculty)


# Faculty handler
@dp.callback_query(UserForm.faculty, F.data.startswith("faculty_"))
async def process_faculty(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    faculty_key = callback_query.data.split("_")[1]
    await state.update_data(faculty=faculty_key)
    await callback_query.answer(f"You selected {faculty_key} faculty.")
    await callback_query.message.edit_text(get_text(lang, 'enter-direction'), reply_markup=direction_buttons(lang))
    await state.set_state(UserForm.direction)


# Direction handler
@dp.callback_query(UserForm.direction, F.data.startswith("direction_"))
async def process_direction(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    direction_key = callback_query.data.split("_")[1]
    await state.update_data(direction=direction_key)
    await callback_query.answer(f"You selected {direction_key} direction.")
    await callback_query.message.edit_text(get_text(lang, 'enter-course'), reply_markup=course_buttons())
    await state.set_state(UserForm.course)


# Course handler
@dp.callback_query(UserForm.course)
async def process_course(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    course_number = callback_query.data.split("_")[1]
    await state.update_data(course=course_number)
    await callback_query.answer(f"You selected {course_number} course.")
    await callback_query.message.edit_text(get_text(lang, "enter-group"), reply_markup=group_buttons())
    await state.set_state(UserForm.group)


# Group handler
@dp.callback_query(UserForm.group, F.data.startswith("group_"))
async def process_group(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    group_number = callback_query.data.split("_")[1]
    await state.update_data(group=group_number)
    await callback_query.answer(f"You selected {group_number} group.")
    await callback_query.message.edit_text(get_text(lang, 'enter-firstname'), reply_markup=None)
    await state.set_state(UserForm.first_name)


# First name handler
@dp.message(UserForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(first_name=message.text)
    await message.answer(get_text(lang, 'enter-lastname'))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.last_name)


# Last name handler
@dp.message(UserForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(last_name=message.text)
    await message.answer(get_text(lang, 'enter-middlename'))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.middle_name)


# Middle name handler
@dp.message(UserForm.middle_name)
async def process_middle_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(middle_name=message.text)
    await message.answer("Muvaffaqiyatli ro'yxatdan o'tdingiz!")
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    data = await state.get_data()
    await Student.objects.filter(telegram_id=user_id).aupdate(
        is_registered=True,
        level=data.get('level'),
        faculty=data.get('faculty'),
        direction=data.get('direction'),
        course=data.get('course'),
        group=data.get('group'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        middle_name=data.get('middle_name')
    )

    await state.clear()

    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(language))

