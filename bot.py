from langchain_community.llms import Ollama
import telebot

API_TOKEN  = '7887777951:AAF_Samfd1QdyAzdsV55gpAfby1N1wctT7s'

bot = telebot.TeleBot(token=API_TOKEN )

# Функция для запуска
def promt(text):
    llm = Ollama(model="llama3.1:8b")
    response = llm.invoke(text)
    return response

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Че те надо")

@bot.message_handler(content_types=['text'])
def send_news(message):
    if message.text.startswith("Бек"):
        bot.reply_to(message, promt(message.text.replace("Бек", " ")))


@bot.message_handler(commands=['stopsrochna'])
def emmm(message):
    exit(0)


bot.polling()