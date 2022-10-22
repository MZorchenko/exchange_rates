import json
import requests
from config import TOKEN_API, exchanges

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, sym, quote):
        sym_key = exchanges[sym.lower()]
        base_key = exchanges[base.lower()]
    
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            quote = float(quote)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {quote}!')
        
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={quote}'
        payload = {}
        headers= {
        "apikey": TOKEN_API
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        r = json.loads(response.text)
        new_price = r['result']
        new_price = round(new_price, 3)
        message =  f"Стоимость {quote} {base} в {sym} : {new_price}"
        return message
