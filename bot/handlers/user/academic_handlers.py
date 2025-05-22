from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user_form import RequestForm
from keyboards.default.menu_keyboard import menu_buttons
from data.scenario import get_text, get_handler_keys
from keyboards.default.common_buttons import request_continue_buttons, request_confirm_buttons
from loader import dp, redis_cl



@dp.message(F.text.in_(get_handler_keys("academic-buttons", 0)))
async def handle_academic_0(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "academic-0"))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 1)))
async def handle_academic_1(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    document_file_id = "BQACAgIAAxkBAAEeU7ZoJPW9rp60KsR-uRqA9VKotiVeDgACc2IAAmy6qUlzsH-ZO57bYjYE"
    await message.answer_document(document=document_file_id)

    photo_file_id = "AgACAgIAAxkBAAEeU7doJPW9mJSU6P8Hwe-LfaHIabfqNQACIewxG2y6qUlMgbwsTriMUwEAAwIAA3kAAzYE"
    await message.answer_photo(photo=photo_file_id, caption=get_text(lang, "academic-1"))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 2)))
async def handle_academic_2(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    video_file_id = "BAACAgIAAxkBAAIV_Ggk_DqQOlEAAUowZUvDTV7RbTB49QAChWIAAmy6qUmJOqsDkEzXgTYE"
    await message.answer_video(video_file_id)


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 3)))
async def handle_academic_3(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="diplom_request")

    await message.answer(get_text(lang, "academic-3"), reply_markup=request_confirm_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 4)))
async def handle_academic_4(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.confirmation)
    await state.update_data(to_service="contract_info")

    await message.answer(get_text(lang, "academic-4"), reply_markup=request_confirm_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 5)))
async def handle_academic_5(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.description)
    await state.update_data(to_service="transcript_paper")

    await message.answer(get_text(lang, "academic-5"), reply_markup=request_continue_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 6)))
async def handle_academic_6(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.description)
    await state.update_data(to_service="gpa_request")

    await message.answer(get_text(lang, "academic-6"), reply_markup=request_continue_buttons(lang))
    
    
@dp.message(F.text.in_(get_handler_keys("academic-buttons", 7)))
async def handle_academic_7(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    await state.set_state(RequestForm.file)
    await state.update_data(to_service="rental_contract")

    await message.answer(get_text(lang, "academic-7"), reply_markup=request_continue_buttons(lang))

    
@dp.message(F.text.in_(get_handler_keys("academic-buttons", 8)))
async def handle_academic_8(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))
    
    