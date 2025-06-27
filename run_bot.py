import asyncio
import os
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from decouple import config

# Load environment variables from .env file
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
DJANGO_API_URL = "http://127.0.0.1:8000/api/create-telegram-user/"
API_SECRET_KEY = config("TELEGRAM_BOT_API_SECRET")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    print(f"Received /start from user: {user.username} (ID: {user.id})")

    user_data = {
        "telegram_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
    }

    headers = {"X-Bot-Secret": API_SECRET_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DJANGO_API_URL, json=user_data, headers=headers
            )

        if response.status_code == 201:
            reply_text = f"Welcome, {user.first_name}! Your profile has been created."
            print(f"Successfully created user {user.username} via API.")
        elif (
            response.status_code == 400
            and "telegram_id" in response.json()
            and "unique" in str(response.json()["telegram_id"])
        ):
            reply_text = f"Welcome back, {user.first_name}! Glad to see you again."
            print(f"User {user.username} already exists.")
        else:
            reply_text = "Sorry, there was an error processing your request."
            print(f"API Error: {response.status_code} - {response.text}")

    except httpx.RequestError as e:
        reply_text = (
            "Sorry, the server is currently unavailable. Please try again later."
        )
        print(f"Failed to connect to Django API: {e}")

    await update.message.reply_text(reply_text)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Telegram bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
