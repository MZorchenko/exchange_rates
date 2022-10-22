import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    faq = "Напишите сообщение боту в виде <имя валюты цену которой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>."
    example = "<b>Например: доллар рубль 500</b>"
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}")
    bot.send_message(message.chat.id, faq)
    bot.send_message(message.chat.id, example, parse_mode='html')
    
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling(none_stop=True)
