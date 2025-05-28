from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default.menu_keyboard import menu_buttons
from keyboards.inline.user_form import level_buttons
from keyboards.inline.common_buttons import language_buttons

from states.user_form import UserForm

from main.models import Student

from data.scenario import get_text
from loader import dp, orm_async, redis_cl


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    exists = await orm_async(Student.objects.filter(telegram_id=user_id).exists)
    if exists:
        student = await orm_async(Student.objects.get, telegram_id=user_id)

        lang = await redis_cl.get(f"user:{user_id}:language")

        if not lang:
            await redis_cl.set(f"user:{user_id}:language", student.language)
            lang = student.language

        if student.is_registered:
            await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))
            return
        else:
            buttons = await level_buttons(lang)
            await message.answer(get_text(lang, "enter-level"), reply_markup=buttons)
            await state.set_state(UserForm.level)
            return

    await message.answer(f"Tilni tanlang / Выберите язык / Select language:", reply_markup=language_buttons)
