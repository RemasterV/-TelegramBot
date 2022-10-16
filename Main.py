import telebot        # импортируем библиотеку для работы с ботом

from Extensions import APIException, CurrenciesConverter # импортируем наши классы
from Config import TOKEN # импортируем наш токен
from Config import dictofcurrencies # импортируем наш словарь валют


bot = telebot.TeleBot(TOKEN) # создаём телеграмм бота

@bot.message_handler(commands=['start','help']) # обрабатываем команды start, help
def helpstart(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой хотите узнать > \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values']) # обрабатываем команду values
def values(message: telebot.types.Message):
    text = 'Валюты для конвертации:'
    for i in dictofcurrencies.keys():
       text = '\n'.join((text, i,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',]) # обрабатываем текстовый запрос, получаем список параметров
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
                    raise APIException('Недопустимое количество параметров')  # исключение, если количество параметров не 3
        quote, base, amount = values
        total = CurrenciesConverter.get_price(quote, base, amount)  # вызываем метод get_price с ранее введёными параметрами
    except APIException as e:
        bot.reply_to(message, f'вы допустили ошибку\n{e}') # выдаём сообщение если ошибка была допущена пользователем
    except Exception as e:
        bot.reply_to(message, f'Ошибка обработки запроса\n{e}') # выдаём сообщение, если случились все что угодно остальное
    else:
        text = f'цена {abs(float(amount))} {quote} в {base}  {round(abs(float(amount)*total),2)}' # выдаём округлёный положительный результат, если всё было обработано корректно
        bot.send_message(message.chat.id, text)


bot.polling() # запускаем бота