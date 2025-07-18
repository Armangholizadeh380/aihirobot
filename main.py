import os
import telebot
import requests

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
bot = telebot.TeleBot(bot_token)

def ask_huggingface(prompt):
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    response = requests.post("https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fa", 
                             headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['translation_text']
    else:
        return "مشکلی پیش آمده است."

@bot.message_handler(func=lambda m: True)
def reply(message):
    user_input = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    result = ask_huggingface(user_input)
    bot.reply_to(message, result)

print("ربات در حال اجراست...")
bot.infinity_polling()
