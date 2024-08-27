import os
import uuid
import string
import random
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the Xnce class for handling Instagram reset logic
class Xnce:
    def __init__(self, target):
        self.target = target
        if self.target[0] == "@":
            return "Enter User Without '@'"
        if "@" in self.target:
            self.data = {
                "_csrftoken": "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)),
                "user_email": self.target,
                "guid": uuid.uuid4(),
                "device_id": uuid.uuid4()
            }
        else:
            self.data = {
                "_csrftoken": "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)),
                "username": self.target,
                "guid": uuid.uuid4(),
                "device_id": uuid.uuid4()
            }
        self.response = self.send_password_reset()

    def send_password_reset(self):
        head = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)"
        }
        req = requests.post("https://i.instagram.com/api/v1/accounts/send_password_reset/", headers=head, data=self.data)
        if "obfuscated_email" in req.text:
            return f"Success: {req.text}"
        else:
            return f"Failed: {req.text}"

# Define command handlers for the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me the Instagram username or email to start the password reset process.')

def handle_message(update: Update, context: CallbackContext) -> None:
    target = update.message.text
    xnce = Xnce(target)
    update.message.reply_text(xnce.response)

def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    """Start the bot."""
    # Replace 'YOUR_TOKEN' with your bot's token
    updater = Updater("6364138523:AAEr27daUr2azrnQkUSeMIJaG0B9D58kaNU")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler for start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler for handling target input
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a stop signal
    updater.idle()

if __name__ == '__main__':
    main()
