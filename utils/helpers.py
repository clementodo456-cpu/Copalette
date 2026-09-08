import io
from PIL import Image
from config import MAX_FILE_SIZE_BYTES, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT, MAX_PIXELS, SUPPORTED_FORMATS

def format_rgb(rgb: tuple[int, int, int]) -> str:
    """Formats RGB tuple as string."""
    return f"{rgb[0]}, {rgb[1]}, {rgb[2]}"

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts HEX string to RGB tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def validate_image_bytes(image_bytes: bytes) -> tuple[bool, str, Image.Image | None]:
    """
    Validates byte content using Pillow.
    Returns (is_valid, error_message, PIL_Image_object).
    """
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        return False, "⚠️ The image file size exceeds the 20 MB limit.", None

    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()  # Verify image structure
        # Re-open after verify() as Pillow recommends
        img = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return False, "❌ Invalid or corrupted image file. Please upload a valid JPG, PNG, or WEBP image.", None

    fmt = (img.format or "").upper()
    if fmt == "JPEG":
        fmt = "JPG"

    if fmt not in SUPPORTED_FORMATS and img.format not in SUPPORTED_FORMATS:
        return False, f"❌ Unsupported image format ({fmt}). Please upload a JPG, PNG, or WEBP image.", None

    width, height = img.size
    total_pixels = width * height

    if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
        return False, f"❌ Image dimensions ({width}x{height}) exceed the maximum allowed size of {MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT} px.", None

    if total_pixels > MAX_PIXELS:
        return False, f"❌ Image resolution is too high ({total_pixels:,} pixels). Maximum allowed is 16,000,000 pixels.", None

    return True, "", img
