from datetime import datetime
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.templatetags.i18n import language
from loader import dp, redis_cl
from keyboards.default.menu_keyboard import academic_menu_buttons, hemis_menu_buttons, settings_buttons, menu_buttons
from keyboards.default.common_buttons import request_cancel_button, weekday_buttons
from data.scenario import get_text, get_handler_keys
from data.schedule import get_schedule

from states.user_form import RequestForm, ScheduleState



@dp.message(F.text.in_(get_handler_keys("menu-buttons", 0)))
async def handle_dars_jadvali(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")

    await state.set_state(ScheduleState.get_day)

    await message.answer(get_text(lang, 'choose-day'), reply_markup=weekday_buttons(lang))
    await message.delete()


@dp.message(ScheduleState.get_day)
async def get_schedule_day(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")

    choosen_day = message.text

    # if choosen_day == get_text(lang, 'today'):
    #     weekday_number = datetime.today().weekday()
    #     response = await get_schedule(user_id, weekday_number)
    # elif choosen_day in get_text(lang, 'weekdays'):
    #     weekday_number = get_text(lang, 'weekdays').index(choosen_day)
    #     response = await get_schedule(user_id, weekday_number)
    # elif choosen_day in get_handler_keys('cancel'):
    #     await state.clear()
    #     await message.answer(get_text(lang, 'menu-message'), reply_markup=menu_buttons(lang))
    #     return
    # else:
    #     await message.answer(get_text(lang, 'wrong-day'), reply_markup=weekday_buttons(lang))
    #     return
    # await message.answer(response, reply_markup=menu_buttons(lang))
    await state.clear()
    await message.answer(get_text(lang, 'schedule-not-found'), reply_markup=menu_buttons(lang))



@dp.message(F.text.in_(get_handler_keys("menu-buttons", 1)))
async def handle_akademik_sorovlar(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "academic-menu"), reply_markup=academic_menu_buttons(lang))
    await message.delete()


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 2)))
async def handle_hemis_sorovlar(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, 'hemis-menu'), reply_markup=hemis_menu_buttons(lang))
    await message.delete()


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 3)))
async def handle_kasallik_malumot(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.description)
    await state.update_data(to_service="illness-inform")

    await message.answer(get_text(lang, "illness-inform"), reply_markup=request_cancel_button(lang))
    await message.delete()


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 4)))
async def handle_settings(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.description)
    await state.update_data(to_service="custom-question")

    await message.answer(get_text(lang, "custom-question"), reply_markup=request_cancel_button(lang))
    await message.delete()

@dp.message(F.text.in_(get_handler_keys("menu-buttons", 5)))
async def handle_settings(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.file)
    await state.update_data(to_service="custom-request")

    await message.answer(get_text(lang, "custom-request"), reply_markup=request_cancel_button(lang))
    await message.delete()


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 6)))
async def handle_settings(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "menu-buttons")[6], reply_markup=settings_buttons(lang))
    await message.delete()


@dp.message(F.text.in_(get_handler_keys("cancel")))
async def handle_cancel(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await state.clear()
    await message.answer(get_text(lang, "cancel-finish"), reply_markup=menu_buttons(lang))