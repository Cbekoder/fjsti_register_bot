from aiogram import F
from aiogram.types import Message
from loader import dp, redis_cl
from keyboards.default.menu_keyboard import (academic_menu_buttons, hemis_menu_buttons, settings_buttons)
from data.scenario import get_text, get_handler_keys

@dp.message(F.text.in_(get_handler_keys("menu-buttons", 0)))
async def handle_dars_jadvali(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 1)))
async def handle_akademik_sorovlar(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "akademik-sorovlar-response"))
    await message.answer("akademik", reply_markup=academic_menu_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 2)))
async def handle_hemis_sorovlar(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "hemis-sorovlar-response"))
    await message.answer('hemis', reply_markup=hemis_menu_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 3)))
async def handle_kasallik_malumot(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer("salkfdj")
    # await message.answer(get_text(lang, "kasallik-malumot-response"))


@dp.message(F.text.in_(get_handler_keys("menu-buttons", 4)))
async def handle_settings(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    await message.answer("Settings", reply_markup=settings_buttons(lang))
    # await message.answer(get_text(lang, "kasallik-malumot-response"))