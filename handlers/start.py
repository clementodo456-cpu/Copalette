from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from keyboards.main import get_start_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 *Welcome to Copalettebot!* (@Copalettebot)\n\n"
    "I extract beautiful, accurate color palettes from any image.\n\n"
    "📌 *Features:*\n"
    "• Supports JPG, PNG, and WEBP images\n"
    "• Handles files up to 20 MB (max 4000x4000 px)\n"
    "• Extracts 3, 5, 7, or 10 dominant colors\n"
    "• Generates downloadable visual palette cards\n"
    "• Exports HEX, RGB, and TXT palette files\n\n"
    "Tap *🎨 Extract Palette* below to get started!"
)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="Markdown"
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Action canceled. Active state cleared.\nSend /start to begin again.",
        reply_markup=get_start_keyboard()
    )

@router.callback_query(F.data == "back_to_start")
async def cb_back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=get_start_keyboard(),
        parse_mode="Markdown"
    )
