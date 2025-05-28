import os
import logging
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.conf import settings
from django.core.files import File
from main.models import StudentRequest, Student
from keyboards.default.menu_keyboard import menu_buttons
from states.user_form import RequestForm
from data.scenario import get_text, get_handler_keys
from keyboards.default.common_buttons import request_continue_buttons
from keyboards.inline.common_buttons import request_confirm_buttons
from loader import dp, redis_cl, orm_async
from asgiref.sync import sync_to_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dp.message(RequestForm.file)
async def handle_file(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    file_id = None

    if message.text == get_text(lang, "continue"):
        await state.set_state(RequestForm.description)
        await message.answer(get_text(lang, "skip-file"), reply_markup=request_continue_buttons(lang))
        return

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name or f"{file_id}.bin"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = f"{file_id}.jpg"
    else:
        await message.answer(get_text(lang, "error-file"), reply_markup=request_continue_buttons(lang))
        return

    if file_id:
        try:
            file = await message.bot.get_file(file_id)
            file_path = file.file_path

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            destination = os.path.join(upload_dir, file_name)
            await message.bot.download_file(file_path, destination)

            if not os.path.exists(destination):
                logger.error(f"File not found after download: {destination}")
                await message.answer(get_text(lang, "error-file-download"), reply_markup=request_continue_buttons(lang))
                return

            await state.update_data(file_path=f"uploads/{file_name}")

            await state.set_state(RequestForm.description)
            await message.answer(get_text(lang, "got-file"), reply_markup=request_continue_buttons(lang))
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {str(e)}")
            await message.answer(get_text(lang, "error-file"), reply_markup=request_continue_buttons(lang))

@dp.message(RequestForm.description)
async def handle_description(message: Message, state: FSMContext):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    if message.text != get_text(lang, "continue"):
        await state.update_data(description=message.text)
    else:
        await state.update_data(description="Izoh yo'q")

    await state.set_state(RequestForm.confirmation)
    await message.answer(get_text(lang, "confirmation"), reply_markup=request_confirm_buttons(lang))

@dp.message(RequestForm.confirmation)
async def handle_confirmation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await message.answer(get_text(lang, "use-buttons"), reply_markup=request_confirm_buttons(lang))


@dp.callback_query(RequestForm.confirmation)
async def handle_confirmation_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer(cache_time=10)
    user_id = callback_query.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")

    if callback_query.data in get_handler_keys("confirm", 0):
        try:
            student = await orm_async(Student.objects.get, telegram_id=user_id)
            data = await state.get_data()
            file_path = data.get("file_path")
            logger.info(f"File path from FSM: {file_path}")

            request = StudentRequest(
                student=student,
                service_slug=data.get("to_service", "default_service"),
                description=data.get("description"),
            )

            if file_path:
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                logger.info(f"Checking file existence: {full_path}")
                if os.path.exists(full_path):
                    with open(full_path, 'rb') as f:
                        await sync_to_async(request.file.save)(os.path.basename(file_path), File(f))
                else:
                    logger.error(f"File not found: {full_path}")

            await sync_to_async(request.save)()

            await state.clear()
            await callback_query.message.answer(
                f"{get_text(lang, 'request-number')}{request.id:05d}\n\n{get_text(lang, 'success')}",
                reply_markup=menu_buttons(lang)
            )
            await callback_query.message.delete()
        except Exception as e:
            logger.error(f"Error creating StudentRequest: {str(e)}")
            await callback_query.message.answer(get_text(lang, "error-request"), reply_markup=menu_buttons(lang))
            await callback_query.message.delete()
            await state.clear()
    else:
        await callback_query.message.edit_text(get_text(lang, "cancel-finish"), reply_markup=menu_buttons(lang))
        await state.clear()