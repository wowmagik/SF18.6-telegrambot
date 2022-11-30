# Написать и протестировать Telegram-бота, в котором будет реализован следующий функционал:
# + Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# + При написании бота необходимо использовать библиотеку pytelegrambotapi.
# + Человек должен отправить сообщение боту в виде <имя валюты цену которой он хочет узнать> <имя валюты в которой
# надо узнать цену первой валюты> <количество первой валюты>.
# + При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
# + При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
# + Для взятия курса валют необходимо использовать API и отправлять к нему запросы с помощью библиотеки Requests.
# + Для парсинга полученных ответов использовать библиотеку JSON.
# + При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число)
# вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
# + Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
# + Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента:
# имя валюты, цену на которую надо узнать, — base, имя валюты, цену в которой надо узнать, — quote, количество
# переводимой валюты — amount и возвращает нужную сумму в валюте.
# + Токен telegramm-бота хранить в специальном конфиге (можно использовать .py файл).
# + Все классы спрятать в файле extensions.py.

import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter, DeclensionByCases

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате:\n <имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты> \n' \
            'Увидеть все доступные валюты /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Количество параметров не совпадает. Используйте формат:\n<имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты> \n')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        inclined_quote = DeclensionByCases(quote, float(amount))
        inclined_base = DeclensionByCases(base, float(total_base))
        quote = inclined_quote.incline()
        base = inclined_base.incline()
        text = f'{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
