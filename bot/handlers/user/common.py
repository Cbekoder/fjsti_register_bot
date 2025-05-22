from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from main.models import Student

from keyboards.default.menu_keyboard import menu_buttons, settings_buttons
from keyboards.inline.user_form import level_buttons
from data.scenario import get_text
from states.user_form import UserForm
from loader import dp, orm_async, redis_cl


@dp.callback_query(F.data.startswith("language"))
async def language_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.message.chat.id
    language = callback_query.data.split("_")[1]
    await callback_query.answer(f"You selected {language} language.")
    student, _ = await orm_async(Student.objects.get_or_create, telegram_id=user_id)

    student.language = language
    student.username = callback_query.message.chat.username

    await redis_cl.set(f"user:{user_id}:language", language)

    await orm_async(student.save)

    if student.is_registered:
        await callback_query.message.answer(get_text(language, "lang-selected"), reply_markup=settings_buttons(language))
        await callback_query.message.delete()
    else:
        buttons = level_buttons(language)
        await callback_query.message.edit_text(get_text(language, "enter-level"), reply_markup=buttons)
        await state.set_state(UserForm.level)