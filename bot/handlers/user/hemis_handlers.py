from aiogram import F
from aiogram.types import Message
from keyboards.default.menu_keyboard import menu_buttons
from data.scenario import get_text, get_handler_keys
from loader import dp, redis_cl


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 0)))
async def handle_hemis_0(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "hemis-0"))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 1)))
async def handle_hemis_1(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 2)))
async def handle_hemis_2(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 3)))
async def handle_hemis_3(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 4)))
async def handle_hemis_4(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 5)))
async def handle_hemis_5(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer("jadval")


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 6)))
async def handle_hemis_6(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")

    video_file_id = "BAACAgIAAxkBAAIU6mgkm1ObMnJTGpy15gYl_7gMelV9AALfYgACbLqpSUIPBtdqHSg5NgQ"

    # await message.bot.send_video(
    #     chat_id=chat_id,
    #     video=video_file_id,
    #     caption="Here is the video you requested!",
    #     parse_mode="MarkdownV2"
    # )
    await message.answer_video(video_file_id)


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 7)))
async def handle_hemis_7(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 8)))
async def handle_hemis_8(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))


@dp.message(F.text.in_(get_handler_keys("hemis-buttons", 9)))
async def handle_hemis_9(message: Message):
    lang = await redis_cl.get(f"user:{message.from_user.id}:language")
    # await message.answer(get_text(lang, "dars-jadvali-response"))
    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))

