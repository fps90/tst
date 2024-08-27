import os
import uuid
import string
import random
import logging
import requests
from telebot import TeleBot, types

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
            self.response = "Enter User Without '@'"
            return
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

# Initialize the bot with your token
bot = TeleBot("6364138523:AAEr27daUr2azrnQkUSeMIJaG0B9D58kaNU")

# Define command handlers for the bot
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome! Send me the Instagram username or email to start the password reset process.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    target = message.text
    xnce = Xnce(target)
    bot.reply_to(message, xnce.response)

# Start the bot
bot.polling()

if __name__ == '__main__':
    bot.polling()
