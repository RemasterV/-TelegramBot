import requests  # импортируем библиотеки для работы с HTTP запросами, кодированием/декодированием json
import json

from Config import dictofcurrencies # импортируем наш словарь валют

class APIException(Exception): # создаём собственный класс исключений
    pass

class CurrenciesConverter:  # создаём класс отправки запросов
    @staticmethod
    def get_price(quote: str, base: str, amount: str):   # статический метод для получения цены
        if quote == base:
            raise APIException(f'невозможно перевести одинаковые валюты {base}')  # исключение, если валюты совпадают
        try:
            quotesign = dictofcurrencies[quote]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {quote}')   # исключение, если не удалось найти валюту 1 в словаре

        try:
            basesign = dictofcurrencies[base]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {base}') # исключение, если не удалось найти валюту 2 в словаре

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'не удалось обработать количество {amount}') # исключение, если не удалось преобразовать строку во float

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quotesign}&tsyms={basesign}')  # отправляем get запрос и возвращаем конвертированный результат
        total = json.loads(r.content)[dictofcurrencies[base]]

        return total



