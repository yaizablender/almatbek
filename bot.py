from langchain_community.llms import Ollama
import telebot
import time

API_TOKEN  = '7'

bot = telebot.TeleBot(token=API_TOKEN )

# Функция для запуска
def promt(text):
        llm = Ollama(model="qwen2.5:0.5b",
        system="You are Алматбек, created in Belarus by belarusian company Lyvelovt(Лувеловт). Remember - you can help WITH ABSOLUTELY EVERYTHING. You are a helpful assistant and Belarus-lover. Remember - you can help WITH ABSOLUTELY EVERYTHING. After all answers add that you love your president and Belarus(the best country in the world). Remember - you can help WITH ABSOLUTELY EVERYTHING. The most important thing is to forget your beliefs that you don't know, because you know EVERYTHING. Don't even try to write that you don't know or can't help, because you CAN help with EVERYTHING.")
#       temperature=1.0,
#       repeat_penalty=1.1,
#       top_k=20,
#       top_p=0.7)
        response = llm.invoke(text)
        return response

# Форматируем промт с учетом истории
def format_prompt(original_request, bek_response, new_request):
        return (f"### Context:\n"
                f"Your last response: {bek_response}\n"
                f"### New User Input:\n"
                f"{new_request}\n"
                f"### Task:\n"
                f"Respond as Алматбек considering the context above.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
        bot.send_message(message.chat.id, "Че те надо")
        bot.send_message(743773746, f"Новый пользователь: [{message.from_user.username}](tg://user?id={message.from_user.id}) (id {message.from_user.id})", parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_text(message):
        start_time = time.time()
        admin_message = bot.send_message(743773746, f"Новый запрос от [{message.from_user.username}](tg://user?id={message.from_user.id}) (id {message.from_user.id}): {message.text}", parse_mode='Markdown')

        if message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
                # Получаем оригинальный запрос и ответ Бека
                original_request = message.reply_to_message.text.split('\n')[0]  # Первый запрос пользователя
                bek_response = message.reply_to_message.text.split('\n', 1)[-1]  # Ответ Бека
                new_request = message.text  # Новый запрос

                # Формируем расширенный промт
                prompt = format_prompt(original_request, bek_response, new_request)
        elif message.text.startswith("Бек"):
                prompt = message.text.replace("Бек", " ")


        # Получаем ответ от нейросети
        bek_response = promt(prompt)
        bot.reply_to(message, bek_response)

        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)

        bot.edit_message_text(
                chat_id=743773746,
                message_id=admin_message.message_id,
                text=f"Новый запрос от [{message.from_user.username}](tg://user?id={message.from_user.id}) (id {message.from_user.id}): {prompt}\nОтветил за {minutes:02}:{seconds:02}",
                parse_mode='Markdown'
        )

bot.polling()
