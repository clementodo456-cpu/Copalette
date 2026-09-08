from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Generates inline buttons for the start menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Extract Palette", callback_data="start_extract")],
            [
                InlineKeyboardButton(text="📖 How It Works", callback_data="how_it_works"),
                InlineKeyboardButton(text="ℹ️ About", callback_data="about_bot")
            ]
        ]
    )

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Generates persistent reply keyboard for cancellation."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/cancel")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
