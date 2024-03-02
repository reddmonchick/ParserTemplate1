import requests
import csv
from loguru import logger
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time
from datetime import datetime
from base_classes.Requests import Requests
from base_classes.Send_data import send_to_core
from base_classes.base_parser import BaseParser
from base_classes.chrome_driver import ChromeDriver
from base_classes.firefox_driver import FirefoxDriver
from base_classes.stop_id_manipulate import StopId
from settings import DEFAULT_STOP_ID


class Parser(BaseParser):

    def __init__(self, parser_name: str):
        self.result_data = {
            'name': parser_name,
            'data': []
        }
        self.StopId: StopId = StopId(default_stop_id=DEFAULT_STOP_ID)  # лучше написать дефолтное значение
        self.new_stop_id = None
        self.send_to_core = send_to_core
        self.driver = FirefoxDriver().get_driver()
        self.request = Requests()
        self.purchase_type = {
            0:'Иной',
            1:"Закупочная сессия",
            2:"Закупка у монополиста",
            3:"Закупочная сессия за право заключения контракта",
            4:"Закупочная сессия с возможностью перехода в закупочную сессию за право заключения контракта"
        }
        self.payment_condition = {
            1: "Оплата при получении",
            2: "В установленный срок",
            3: "Предоплата",
            4: "Регулярная оплата"
        }
    def run(self):
        for page_num in range(1, 80): # определяем самостоятельно в зависимости от сайта и сколько максимално страниц, предназначен для то что если стоп условие не сработает парсер не ушел в бесконечный парсинг

            json_items: tuple = self.get_tender_links_from_page(page_num) # Получаем ссылки на карточки
            for item in json_items:
                search_dct,card_dct = item # карточки из поиска и сама карточка
                self.id = search_dct.get('id','')

                customer,contactperson = self.get_customer_and_contactperson(card_dct)

                terms_of_payment_part1 = card_dct.get('trade',{}).get('lot',{}).get('paymentDateInDays','')
                terms_of_payment_part2 = self.payment_condition.get(card_dct.get('trade',{}).get('lot',{}).get('paymentCondition',''),'')

                procedure_info = self.get_procedureinfo([search_dct.get('trade',{}).get('publishDate',''),
                                                         search_dct.get('trade',{}).get('applicationFillingStartDate',''),
                                                         search_dct.get('trade',{}).get('applicationFillingEndDate','')])

                lots = self.create_lots(addi_info=card_dct.get('lot',{}).get('additionalConditions',''),deli_place=card_dct.get())

                documents = card_dct.get('documents')

                tender = {
                        'purchaseNumber': str(search_dct.get('tradeNumber')),
                        'procurementStage': 'Подача предложений', # Фиксированное значение т.к. в ссылке везде такое значение
                        'customer': customer,
                        'contactPerson':contactperson,
                        'title': card_dct.get('lot',{}).get('subject'),
                        'purchaseType': self.purchase_type.get(card_dct.get('trade',{}).get('purchaseMethod',''),''),
                        'terms_of_payment': f'{terms_of_payment_part1}{terms_of_payment_part2}'.strip(),
                        'price': search_dct.get('price'),
                        'obesp_z': search_dct.get('applicationGuarantee'),
                         'procedureInfo': procedure_info,
                        'startDateContract': self.normalize_date(card_dct), # Дата заключения контракта # Используем метод,что бы сделать дату по формату
                        'deliveryTerm': self.get_delivery_term(card_dct),
                        'attachments' : self.get_attachment(card_dct)
                        }

                self.result_data['data'].append(tender)
                if len(self.result_data['data']) > 10:
                    self.send_to_core(self.result_data)
                    self.result_data['data'].clear()

        self.StopId.update_stop_id(self.new_stop_id)

    def get_attachments(self,dct: dict) -> list:
        docs = dct.get('trade',{}).get('lot',{}).get('documents',[])
        filtered_docs = [{"url": self.create_fileupload_url(item)} for item in docs if item.get('type') == 4] # Фильтруем нужные нам документы
        return filtered_docs

    def create_fileupload_url(self,dct:dict) -> str:
        type,id = dct.get('type',''),dct.get('id','')
        if id and type:
            doc_url = f'https://tender-api.agregatoreat.ru/api/FileUpload/{self.id}/{type}/{id}'
            return doc_url
        else:
            return ''

    def get_delivery_term(self,dct: dict) -> str:
        type = dict.get('deliveryType')
        pass

    def create_lots(self,addi_info: str,deli_place: str,reg:str) -> dict:
        pass
    def get_customer_and_contactperson(self,dct: dict) -> dict: # Получаем customer и contactPerson
        dct = dct.get('customer',{})
        customer_ = {}
        contactperson_ = {}
        customer_['fullName'] = dct.get('name','')
        customer_['inn'] = dct.get('inn','')
        customer_['kkp'] = dct.get('kpp','')
        customer_['factAddress'] = dct.get('address','')

        fio = dct.get('contactFio','').split()
        if fio:
            contactperson_['lastName'] = fio[0] # last_name
            contactperson_['firstName'] = fio[1] # first_name
            contactperson_['middleName'] = fio[2] # middlename
        contactperson_['contactEmail'] = dct.get('contactEmail','') #contactemail
        contactperson_['contactPhone'] = dct.get('contactPhone','') #contactphone
        return customer_,contactperson_

    def get_procedureinfo(self,lst: list) -> dict:
        proced_info = {}
        lst = list(map(lambda x: self.normalize_date(x) ,lst)) # normalize_date форматирует дату в таком виде 01:11:00 25.01.2023
        proced_info['publishedDate'] = lst[0]
        proced_info['startDate'] = lst[1]
        proced_info['endDate'] = lst[2]
        return proced_info

    def normalize_date(self,dct:dict)-> str:
        original_date = dct.get('trade', {}).get('lot', {}).get('contractSignDate', '')
        if not original_date:
            return ''
        else:
            original_date = datetime.fromisoformat(original_date)
            # Форматирование даты и времени в нужный формат
            formatted_date = original_date.strftime("%H:%M:%S %d.%m.%Y")
            return formatted_date


if __name__=="__main__":
    Parser('vk').run()
