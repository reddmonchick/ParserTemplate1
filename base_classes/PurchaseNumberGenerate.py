import json
import os

import requests

from custom_exceptions.parse_error import RequestError


class PurchaseNumberGenerator:
    '''
    Передаем имя парсера и вызываем метод get() более ничего делать не надо
    '''
    __slots__ = ("new_purchase_numbers", "parser_name")

    def __init__(self, parser_name):
        self.parser_name = parser_name
        self.new_purchase_numbers: list = []
        self.__request_to_purchase_number_generator()

    def get(self) -> list:
        try:
            value = self.new_purchase_numbers.pop()
        except:
            self.__request_to_purchase_number_generator()
            value = self.new_purchase_numbers.pop()
        return value

    def __request_to_purchase_number_generator(self):
        headers = {"Content-Type": 'application/json'}
        response = requests.get(url=os.getenv("PURCHASE_NUMBER_GENERATOR_URL"), headers=headers, data=json.dumps(
            {'parser': self.parser_name}
        ))
        if response.status_code == 200:
            values: list = response.json().get('purchase_numbers')
            values.reverse()
            self.new_purchase_numbers = values
        else:
            raise RequestError(f"not valid request to purchase number generator, msg: {response.__dict__}")
