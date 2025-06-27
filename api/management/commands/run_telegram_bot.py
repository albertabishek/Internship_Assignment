import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from api.models import TelegramUser
from asgiref.sync import sync_to_async

# Use sync_to_async to wrap the database call
@sync_to_async
def get_or_create_user(user_data):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=user_data.id,
        defaults={
            'first_name': user_data.first_name,
            'username': user_data.username
        }
    )
    return user, created

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command. Collects user info and saves to DB."""
    user = update.effective_user 
    print(f"Received /start command from user: {user.username} (ID: {user.id})")

    tg_user, created = await get_or_create_user(user)

    if created:
        reply_text = f"Welcome, {user.first_name}! Your profile has been created in our database."
        print(f"Existing user '{user.username}' interacted with the bot.")

    await update.message.reply_text(reply_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"You said: {update.message.text}")


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot...'))

        # Create the Application and pass it your bot's token.
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("start", start))

        # on non command i.e message - echo the message on Telegram 
        application.add_handler(MessageHandler(filter.TEXT & ~filters.COMMAND, echo))

        # Run the bot until the user presses Ctrl-C
        application.run_polling()

        self.stdout.write(self.style.SUCCESS('Telegram bot stopped.'))
