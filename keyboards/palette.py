from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_color_count_keyboard() -> InlineKeyboardMarkup:
    """Generates options for choosing palette count."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="3 Colors", callback_data="count_3"),
                InlineKeyboardButton(text="5 Colors", callback_data="count_5")
            ],
            [
                InlineKeyboardButton(text="7 Colors", callback_data="count_7"),
                InlineKeyboardButton(text="10 Colors", callback_data="count_10")
            ],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_start")]
        ]
    )

def get_output_options_keyboard() -> InlineKeyboardMarkup:
    """Generates result action buttons."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Palette Image", callback_data="out_image"),
                InlineKeyboardButton(text="📄 Export TXT", callback_data="out_txt")
            ],
            [
                InlineKeyboardButton(text="🔤 HEX Codes", callback_data="out_hex"),
                InlineKeyboardButton(text="🔢 RGB Codes", callback_data="out_rgb")
            ],
            [InlineKeyboardButton(text="🔄 Extract Again", callback_data="start_extract")]
        ]
    )
