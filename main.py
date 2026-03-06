
import telebot
import requests
import os

# TOKEN DIRECTO (cambia por tuyo)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8000550010:AAHJrXGZZSGZNdT2OOq8bTYFxqr1rB2zqD8")  # fallback
if not TOKEN:
    print("ERROR: TOKEN vacío!")
    exit(1)

bot = telebot.TeleBot(TOKEN)
print("Bot iniciado con TOKEN:", TOKEN[:10] + "..." )  # debug

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 PolyBot Live! /poly")

@bot.message_handler(commands=['poly'])
def poly(message):
    try:
        r = requests.get('https://gamma.api.polymarket.com/markets?active=true&limit=10&sort=volume', timeout=30)
        data = r.json()
        msg = "🏆 TOP POLYMARKET VALUE BETS:\n"
        for m in data[:3]:
            yes = m.get('yes_price', 0.5)
            value = max(1 - yes, yes) - 0.15
            if value > 0:
                msg += f"• {m['question'][:40]}: {value:.1%}\n"
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

print("Polling...")
bot.polling(none_stop=True)
