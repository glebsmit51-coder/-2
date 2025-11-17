import os
import telebot
from telebot import types
import json
import datetime

def main():
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = telebot.TeleBot(BOT_TOKEN)
    
    # Твой основной код бота здесь
    
    print("🤖 Бот запущен в облаке...")
    bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()
