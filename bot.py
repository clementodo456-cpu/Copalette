import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, PORT, LOG_LEVEL
from handlers import start, palette, help

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("copalettebot")

async def health_check_handler(request: web.Request) -> web.Response:
    """Render web service health check endpoint."""
    return web.Response(text="Copalettebot is running", status=200)

async def start_health_server() -> web.AppRunner:
    """Starts concurrent lightweight HTTP server for Render binding."""
    app = web.Application()
    app.router.add_get("/", health_check_handler)
    app.router.add_get("/health", health_check_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Health server successfully bound to 0.0.0.0:{PORT}")
    return runner

async def main():
    logger.info("Initializing Copalettebot...")

    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register router handlers
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(palette.router)

    # Start Health Check Server concurrently
    runner = await start_health_server()

    try:
        logger.info("Starting Telegram long polling...")
        # Delete webhook before polling to clear conflicts
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        logger.info("Shutting down bot and server...")
        await runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot execution terminated.")
