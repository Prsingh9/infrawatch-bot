# test_telegram.py
from alerts.telegram_alert import TelegramAlert

bot = TelegramAlert("8776804198:AAGIqG-W15KO3kvn_j5y4h1jS9jO-vrEwHE", "951397096")
bot.send("🟢 *InfraWatch Bot is alive!*")
