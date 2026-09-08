from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import MAX_FILE_SIZE_BYTES
from keyboards.palette import get_color_count_keyboard, get_output_options_keyboard
from keyboards.main import get_start_keyboard
from utils.helpers import validate_image_bytes
from services.color_extractor import extract_palette
from services.palette_generator import generate_palette_image

router = Router()

class PaletteState(StatesGroup):
    waiting_for_image = State()
    waiting_for_color_count = State()

@router.message(Command("palette"))
@router.callback_query(F.data == "start_extract")
async def prompt_image_upload(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(PaletteState.waiting_for_image)
    text = (
        "📥 *Upload an Image*\n\n"
        "Please send a photo or document image (JPG, PNG, or WEBP).\n"
        "• Max file size: 20 MB\n"
        "• Max resolution: 4000 x 4000 px"
    )
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(text, parse_mode="Markdown")
    else:
        await event.answer(text, parse_mode="Markdown")

@router.message(PaletteState.waiting_for_image, F.photo | F.document)
async def process_uploaded_image(message: Message, state: FSMContext, bot: Bot):
    file_id = None
    file_size = 0

    if message.photo:
        # Take highest resolution photo
        photo = message.photo[-1]
        file_id = photo.file_id
        file_size = photo.file_size or 0
    elif message.document:
        mime = message.document.mime_type or ""
        if not (mime.startswith("image/") or message.document.file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))):
            await message.answer("❌ Invalid document type. Please upload an image file (JPG, PNG, or WEBP).")
            return
        file_id = message.document.file_id
        file_size = message.document.file_size or 0

    if file_size > MAX_FILE_SIZE_BYTES:
        await message.answer("⚠️ File size exceeds the 20 MB limit. Please upload a smaller file.")
        return

    status_msg = await message.answer("⏳ Downloading image...")

    try:
        tg_file = await bot.get_file(file_id)
        if (tg_file.file_size or 0) > MAX_FILE_SIZE_BYTES:
            await status_msg.edit_text("⚠️ File size exceeds the 20 MB limit. Download aborted.")
            return

        downloaded_bytes = await bot.download_file(tg_file.file_path)
        image_bytes = downloaded_bytes.read()

        await status_msg.edit_text("🔍 Validating image...")
        is_valid, error_msg, _ = validate_image_bytes(image_bytes)

        if not is_valid:
            await status_msg.edit_text(error_msg)
            return

        # Store image in FSM memory buffer
        await state.update_data(image_bytes=image_bytes)
        await state.set_state(PaletteState.waiting_for_color_count)

        await status_msg.edit_text(
            "⚙️ *Choose Palette Size*\n\nSelect how many dominant colors you would like to extract:",
            reply_markup=get_color_count_keyboard(),
            parse_mode="Markdown"
        )

    except Exception as e:
        await status_msg.edit_text("❌ An error occurred while downloading or validating the image. Please try again.")

@router.message(PaletteState.waiting_for_image)
async def process_invalid_image_input(message: Message):
    await message.answer("⚠️ Please upload a valid image file or use /cancel to stop.")

@router.callback_query(PaletteState.waiting_for_color_count, F.data.startswith("count_"))
async def process_palette_generation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    count = int(callback.data.split("_")[1])
    data = await state.get_data()
    image_bytes = data.get("image_bytes")

    if not image_bytes:
        await callback.message.edit_text("⚠️ Session expired. Please upload your image again.", reply_markup=get_start_keyboard())
        await state.clear()
        return

    status_msg = callback.message
    await status_msg.edit_text("🎨 Analyzing colors...")

    try:
        is_valid, _, img = validate_image_bytes(image_bytes)
        if not is_valid or img is None:
            await status_msg.edit_text("❌ Image processing error. Please try uploading again.")
            await state.clear()
            return

        palette = extract_palette(img, num_colors=count)

        await status_msg.edit_text("✨ Building your palette...")
        palette_image_bytes = generate_palette_image(img, palette)

        # Build text summary
        text_lines = ["🎨 *Your Color Palette*\n"]
        for idx, (hex_code, rgb) in enumerate(palette, 1):
            text_lines.append(f"*{idx}. {hex_code}*")
            text_lines.append(f"   RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}\n")

        summary_text = "\n".join(text_lines)

        # Save results in state for output actions
        await state.update_data(
            palette=palette,
            palette_image_bytes=palette_image_bytes,
            summary_text=summary_text
        )

        photo_file = BufferedInputFile(palette_image_bytes, filename="palette.png")
        await callback.message.channel_post or callback.message.answer_photo(
            photo=photo_file,
            caption=summary_text,
            reply_markup=get_output_options_keyboard(),
            parse_mode="Markdown"
        )
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ Failed to generate palette. Please try another image.")
        await state.clear()

@router.callback_query(F.data == "out_image")
async def cb_output_image(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    palette_image_bytes = data.get("palette_image_bytes")

    if not palette_image_bytes:
        await callback.answer("⚠️ Session active data not found. Extract a new palette.", show_alert=True)
        return

    await callback.answer()
    photo_file = BufferedInputFile(palette_image_bytes, filename="palette.png")
    await callback.message.answer_photo(photo=photo_file, caption="🎨 Color Palette Image Preview")

@router.callback_query(F.data == "out_txt")
async def cb_output_txt(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    palette = data.get("palette")

    if not palette:
        await callback.answer("⚠️ Session active data not found. Extract a new palette.", show_alert=True)
        return

    await callback.answer()
    txt_content = "Copalettebot - Color Palette Export\n"
    txt_content += "=" * 35 + "\n\n"

    for idx, (hex_code, rgb) in enumerate(palette, 1):
        txt_content += f"Color {idx}:\n"
        txt_content += f"  HEX: {hex_code}\n"
        txt_content += f"  RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}\n\n"

    txt_file = BufferedInputFile(txt_content.encode('utf-8'), filename="palette.txt")
    await callback.message.answer_document(document=txt_file, caption="📄 Exported Color Palette TXT")

@router.callback_query(F.data == "out_hex")
async def cb_output_hex(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    palette = data.get("palette")

    if not palette:
        await callback.answer("⚠️ Session active data not found.", show_alert=True)
        return

    await callback.answer()
    hex_list = "\n".join([f"`{hex_code}`" for hex_code, _ in palette])
    await callback.message.answer(f"🔤 *HEX Codes:*\n\n{hex_list}", parse_mode="Markdown")

@router.callback_query(F.data == "out_rgb")
async def cb_output_rgb(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    palette = data.get("palette")

    if not palette:
        await callback.answer("⚠️ Session active data not found.", show_alert=True)
        return

    await callback.answer()
    rgb_list = "\n".join([f"`{rgb[0]}, {rgb[1]}, {rgb[2]}`" for _, rgb in palette])
    await callback.message.answer(f"🔢 *RGB Codes:*\n\n{rgb_list}", parse_mode="Markdown")
