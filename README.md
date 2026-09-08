# 🎨 Copalettebot (@Copalettebot)

A production-ready Telegram bot built with **Python 3.13**, **aiogram 3.x**, and **Pillow** that extracts clean, visual color palettes from uploaded images.

---

## ✨ Features

- 🖼️ **Multi-Format Support**: Process JPG, PNG, and WEBP images.
- 🎨 **Custom Palette Size**: Choose 3, 5, 7, or 10 dominant colors.
- 📐 **Smart Color Clustering**: Automatically reduces duplicate/similar shades for distinct palette output.
- 🖼️ **Visual Palette Cards**: Generates high-resolution PNG previews with swatches and color codes.
- 📄 **Multiple Exports**: Export via Palette Image, HEX codes, RGB codes, or `.txt` download.
- 🔒 **Privacy First**: Processed in-memory; images are never permanently stored on servers.

---

## ⚙️ Limits & Constraints

- **Max File Size**: 20 MB
- **Max Dimensions**: 4000 x 4000 px
- **Max Resolution**: 16,000,000 pixels

---

## 🛠️ BotFather Setup

1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the instructions to name your bot (e.g., `Copalettebot`).
3. Copy the HTTP API **Token**.
4. Set bot command menu via `/setcommands`:
   ```text
   start - Start the bot & show main menu
   palette - Extract palette from an image
   help - How it works & supported formats
   about - Learn about Copalettebot
   cancel - Cancel active operation
