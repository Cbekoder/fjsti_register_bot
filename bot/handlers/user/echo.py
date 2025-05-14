from aiogram.types import Message, ContentType
import json
from aiogram import F
from loader import dp, router

# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#         try:
#             # Parse the JSON string into a dictionary
#             message_data = json.loads(message.json())
#
#             # Filter out fields with None values
#             filtered_data = {key: value for key, value in message_data.items() if value is not None}
#
#             # Send the filtered data as a response
#             await message.answer(json.dumps(filtered_data, indent=2), parse_mode="Markdown")
#         except (TypeError, json.JSONDecodeError):
#             # Handle unsupported message types or invalid JSON
#             await message.answer("Unable to process the message!")
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")
#

@router.message(F.content_type == ContentType.VIDEO)
async def video_handler(message: Message) -> None:
    """
    Handler will forward received video messages back to the sender.

    By default, this handler will process video messages.
    """
    try:
        # Send a copy of the received video message
        await message.send_copy(chat_id=message.chat.id)
        try:
            # Parse the JSON string into a dictionary
            message_data = json.loads(message.json())

            # Filter out fields with None values
            filtered_data = {key: value for key, value in message_data.items() if value is not None}

            # Escape special characters for MarkdownV2
            escaped_json = json.dumps(filtered_data, indent=2)
            escaped_json = (
                escaped_json.replace("_", "\\_")
                .replace("*", "\\*")
                .replace("[", "\\[")
                .replace("]", "\\]")
                .replace("`", "\\`")
                .replace("{", "\\{")
                .replace("}", "\\}")
                .replace("(", "\\(")
                .replace(")", "\\)")
                .replace(">", "\\>")
                .replace("#", "\\#")
                .replace("+", "\\+")
                .replace("-", "\\-")
                .replace(".", "\\.")
                .replace("!", "\\!")
            )

            # Send the filtered data as a response
            await message.answer(escaped_json, parse_mode="MarkdownV2")
        except (TypeError, json.JSONDecodeError):
            # Handle unsupported message types or invalid JSON
            await message.answer("Unable to process the video message!")
    except TypeError:
        # Handle unsupported message types for copying
        await message.answer("Nice try!")