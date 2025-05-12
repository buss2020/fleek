import os
import time
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = "8088298395:AAGk_RnklTLQS9IkRRMdYn3fQumK50X3HPc"
CHAT_ID = 8088298395
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

def simple_agent_response(text):
    if "привет" in text.lower():
        return "Привет! Чем могу помочь?"
    elif "как дела" in text.lower():
        return "У меня всё отлично, я бот!"
    else:
        return f"Ты написал: {text}"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    reply = simple_agent_response(text)
    bot.send_message(chat_id=chat_id, text=reply)
    return 'ok'

@app.route("/start_loop")
def start_loop():
    def auto_loop():
        while True:
            bot.send_message(chat_id=CHAT_ID, text="Привет, агент!")
            time.sleep(30)
    import threading
    threading.Thread(target=auto_loop).start()
    return "Loop started"

@app.route("/")
def index():
    return "Telegram self-agent is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
