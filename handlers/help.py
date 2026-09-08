from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

router = Router()

HOW_IT_WORKS_TEXT = (
    "📖 *How It Works*\n\n"
    "1️⃣ Send an image as a photo or uncompressed document (JPG, PNG, WEBP up to 20 MB).\n"
    "2️⃣ Select how many dominant colors you want to extract (3, 5, 7, or 10).\n"
    "3️⃣ The bot processes your image using smart color quantization and distinction algorithms.\n"
    "4️⃣ Receive your clean color palette image along with exact HEX and RGB color values!"
)

ABOUT_TEXT = (
    "ℹ️ *About Copalettebot*\n\n"
    "Copalettebot (@Copalettebot) is a fast, precise tool designed for designers, developers, and creators.\n\n"
    "⚡ Built with Python 3.13, aiogram 3.x, and Pillow.\n"
    "🔒 Privacy guaranteed: Uploaded images are processed in-memory and immediately destroyed.\n"
    "🚀 Deployed on Render."
)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HOW_IT_WORKS_TEXT, parse_mode="Markdown")

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(ABOUT_TEXT, parse_mode="Markdown")

@router.callback_query(F.data == "how_it_works")
async def cb_how_it_works(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(HOW_IT_WORKS_TEXT, parse_mode="Markdown")

@router.callback_query(F.data == "about_bot")
async def cb_about(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(ABOUT_TEXT, parse_mode="Markdown")
