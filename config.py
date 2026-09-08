import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing! Please set it in .env or environment.")

PORT: int = int(os.getenv("PORT", "8080"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Constraints
MAX_FILE_SIZE_BYTES: int = 20 * 1024 * 1024  # 20 MB
MAX_IMAGE_WIDTH: int = 4000
MAX_IMAGE_HEIGHT: int = 4000
MAX_PIXELS: int = 16_000_000
SUPPORTED_FORMATS: set[str] = {"JPEG", "JPG", "PNG", "WEBP"}
