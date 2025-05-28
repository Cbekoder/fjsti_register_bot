from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.default.menu_keyboard import menu_buttons, hemis_menu_buttons
from states.user_form import RequestForm
from data.scenario import get_text, get_handler_keys
from keyboards.default.common_buttons import request_continue_buttons, request_cancel_button
from keyboards.inline.common_buttons import request_confirm_buttons
from loader import dp, redis_cl, orm_async



@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 0)))
async def handle_hemis_0(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="recover_password")

    await message.answer(get_text(lang, "hemis-0"), reply_markup=request_confirm_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 1)))
async def handle_hemis_1(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.file)
    await state.update_data(to_service="changing_personal_data")

    await message.answer(get_text(lang, "hemis-1"), reply_markup=request_cancel_button(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 2)))
async def handle_hemis_2(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="study_information")

    video_file_id = "BAACAgIAAxkBAAICrGgoIFXxDn4iUglr3qD2ZG99gXfSAALXYgACbLqpSRrUAzXrcP_JNgQ"

    await message.answer_video(video=video_file_id)

    await message.answer(get_text(lang, "hemis-2"), reply_markup=request_confirm_buttons(lang))



@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 3)))
async def handle_hemis_3(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="rating_record")

    video_file_id = "BAACAgIAAxkBAAICsmgoIo2ChR2UQUs1cdiMMl3zYt66AAK4YgACbLqpSTFG2E-1IyoBNgQ"
    await message.answer_video(video=video_file_id)

    await message.answer(get_text(lang, "hemis-3"), reply_markup=request_confirm_buttons(lang))



@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 4)))
async def handle_hemis_4(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="attendance")

    video_file_id = "BAACAgIAAxkBAAICrGgoIFXxDn4iUglr3qD2ZG99gXfSAALXYgACbLqpSRrUAzXrcP_JNgQ"
    await message.answer_video(video=video_file_id)

    await message.answer(get_text(lang, "hemis-4"), reply_markup=request_confirm_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 5)))
async def handle_hemis_5(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    video_file_id = "BAACAgIAAxkBAAIU5mgkm1ObMnJTGpy15gYl_7gMelV9AALfYgACbLqpSUIPBtdqHSg5NgQ"
    await message.answer_video(video_file_id)


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 6)))
async def handle_hemis_6(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="graduation_paper")

    await message.answer(get_text(lang, "hemis-6"), reply_markup=request_confirm_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 7)))
async def handle_hemis_7(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    video_file_id = "BAACAgIAAxkBAAIWDmgk_n2onB09mypEYLneQlneu3z_AALdYgACbLqpSQ2EeQIujmPhNgQ"
    await message.answer_video(video_file_id)


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 8)))
async def handle_hemis_8(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))

