from aiogram import F
from aiogram.types import Message
from keyboards.default.menu_keyboard import menu_buttons
from data.scenario import get_text, get_handler_keys
from loader import dp, redis_cl




@dp.message(F.text.in_(get_handler_keys("academic-buttons", 0)))
async def handle_academic_0(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "academic-0"))


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 1)))
async def handle_academic_1(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")



@dp.message(F.text.in_(get_handler_keys("academic-buttons", 2)))
async def handle_academic_2(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 3)))
async def handle_academic_3(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("academic-buttons", 4)))
async def handle_academic_4(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")
    
    
@dp.message(F.text.in_(get_handler_keys("academic-buttons", 5)))
async def handle_academic_5(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")
    
    
@dp.message(F.text.in_(get_handler_keys("academic-buttons", 6)))
async def handle_academic_6(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))
    
    