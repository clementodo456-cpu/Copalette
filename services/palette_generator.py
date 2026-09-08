import io
from PIL import Image, ImageDraw, ImageFont

def generate_palette_image(
    original_img: Image.Image,
    palette: list[tuple[str, tuple[int, int, int]]]
) -> bytes:
    """
    Generates a clean, modern palette layout containing swatches, hex codes, RGB values,
    and a small preview of the original image.
    """
    width = 1000
    swatch_height = 100
    padding = 24
    num_colors = len(palette)

    # Calculate layout dimensions
    preview_size = 280
    palette_section_width = width - (padding * 3) - preview_size
    header_height = 80
    palette_height = (swatch_height * num_colors) + (padding * (num_colors - 1))
    content_height = max(preview_size, palette_height)
    total_height = header_height + content_height + (padding * 2)

    # Create canvas
    canvas = Image.new("RGB", (width, total_height), "#0F172A")  # Dark Slate Background
    draw = ImageDraw.Draw(canvas)

    # Load fonts (fallback to default if custom unavailable)
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        font_hex = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        font_rgb = ImageFont.truetype("DejaVuSans.ttf", 16)
    except IOError:
        font_title = ImageFont.load_default()
        font_hex = ImageFont.load_default()
        font_rgb = ImageFont.load_default()

    # Draw Title Header
    draw.text((padding, padding), "🎨 Color Palette", fill="#F8FAFC", font=font_title)
    draw.line(
        [(padding, header_height - 10), (width - padding, header_height - 10)],
        fill="#334155",
        width=2
    )

    # Prepare and paste preview image
    preview = original_img.copy()
    if preview.mode != "RGB":
        preview = preview.convert("RGB")
    preview.thumbnail((preview_size, preview_size), Image.Resampling.LANCZOS)
    
    # Create square container for preview
    preview_box = Image.new("RGB", (preview_size, preview_size), "#1E293B")
    offset_x = (preview_size - preview.width) // 2
    offset_y = (preview_size - preview.height) // 2
    preview_box.paste(preview, (offset_x, offset_y))
    
    canvas.paste(preview_box, (padding, header_height))

    # Draw Palette Swatches
    start_x = padding * 2 + preview_size
    start_y = header_height

    for i, (hex_code, rgb) in enumerate(palette):
        y = start_y + i * (swatch_height + padding)

        # Draw Swatch Box
        swatch_width = 120
        draw.rectangle(
            [start_x, y, start_x + swatch_width, y + swatch_height],
            fill=hex_code,
            outline="#475569",
            width=1
        )

        # Draw Card Background for details
        detail_x = start_x + swatch_width + 16
        detail_width = palette_section_width - swatch_width - 16
        draw.rectangle(
            [detail_x, y, detail_x + detail_width, y + swatch_height],
            fill="#1E293B",
            outline="#334155",
            width=1
        )

        # Text labels
        draw.text((detail_x + 20, y + 20), hex_code, fill="#F8FAFC", font=font_hex)
        draw.text(
            (detail_x + 20, y + 55),
            f"RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}",
            fill="#94A3B8",
            font=font_rgb
        )

    output = io.BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    return output.getvalue()
