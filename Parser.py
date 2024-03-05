import requests
import csv
from loguru import logger
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time
from datetime import datetime
from base_classes.Requests import Requests
#from base_classes.Send_data import send_to_core
from base_classes.base_parser import BaseParser
from base_classes.chrome_driver import ChromeDriver
from base_classes.firefox_driver import FirefoxDriver
from base_classes.stop_id_manipulate import StopId
from settings import DEFAULT_STOP_ID
from dotenv import load_dotenv
import os
import redis

class Parser(BaseParser):

    def __init__(self, parser_name: str):
        load_dotenv()
        self.core_url = os.getenv("VALIDATOR_URL")

        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.redis_client.config_set('save', '60 1')
        self.ttl_seconds = 24 * 60 * 60  # 1 день в секундах
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
        logger.info('Запустили функцию парсинга(run)')
        for page_num in range(1, 80): # определяем самостоятельно в зависимости от сайта и сколько максимално страниц, предназначен для то что если стоп условие не сработает парсер не ушел в бесконечный парсинг

            json_items: tuple = self.get_tender_links_from_page(page_num) # Получаем ссылки на карточки
            for item in json_items:
                search_dct,card_dct = item # карточки из поиска и сама карточка
                self.id = search_dct.get('id','')
                if not self.redis_client.exists(self.id):
                    # Если ссылка ещё не была обработана, выполняем парсинг и сохраняем результат
                    logger.info(f'Обрабатываем ссылку https://agregatoreat.ru/purchases/announcement/{self.id}')

                    customer, contactperson = self.get_customer_and_contactperson(card_dct)

                    terms_of_payment_part1 = card_dct.get('trade', {}).get('lot', {}).get('paymentDateInDays', '')
                    terms_of_payment_part2 = self.payment_condition.get(
                        card_dct.get('trade', {}).get('lot', {}).get('paymentCondition', ''), '')

                    procedure_info = self.get_procedureinfo([search_dct.get('trade', {}).get('publishDate', ''),
                                                             search_dct.get('trade', {}).get(
                                                                 'applicationFillingStartDate', ''),
                                                             search_dct.get('trade', {}).get(
                                                                 'applicationFillingEndDate', '')])

                    lots = self.create_lots(dct=card_dct.get('trade', {}).get('lot', {}))

                    documents = card_dct.get('documents')

                    tender = {
                        'purchaseNumber': str(search_dct.get('tradeNumber')),
                        'procurementStage': 'Подача предложений',
                        # Фиксированное значение т.к. в ссылке везде такое значение
                        'customer': customer,
                        'contactPerson': contactperson,
                        'title': card_dct.get('lot', {}).get('subject'),
                        'purchaseType': self.purchase_type.get(card_dct.get('trade', {}).get('purchaseMethod', ''), ''),
                        'terms_of_payment': f'{terms_of_payment_part1}{terms_of_payment_part2}'.strip(),
                        'price': search_dct.get('price'),
                        'obesp_z': search_dct.get('applicationGuarantee'),
                        'procedureInfo': procedure_info,
                        'startDateContract': self.normalize_date(card_dct),
                        # Дата заключения контракта # Используем метод,что бы сделать дату по формату
                        'deliveryTerm': self.get_delivery_term(card_dct),
                        'attachments': self.get_attachment(card_dct),
                        'lots': lots
                    }

                    self.result_data['data'].append(tender)
                    self.send_to_core(self.result_data)
                    self.result_data['data'].clear()
                    # Добавляем ID ссылки в Redis для отметки того, что она была обработана
                    self.redis_client.set(self.id, 1)
                    self.redis_client.expire(self.id,self.ttl_seconds)
                else:
                    logger.info(f'НЕ Обрабатываем ссылку(она уже есть в бд) https://agregatoreat.ru/purchases/announcement/{self.id}')
        logger.info('Закончили функцию парсинга(run)')
        self.StopId.update_stop_id(self.new_stop_id)

    def send_to_core(self,result_data: dict) -> None:
        json_ = json.dumps(result_data)
        res = requests.post(
            url=self.core_url,
            data=json_,
            headers={'Content-Type': 'application/json'},
        )
        if res.status_code == 200:
            logger.info("response status 200, success")
        else:
            logger.error(f'response status: {res.status_code}')

    def create_lots(self, dct: dict) -> list:
        addt_info = dct.get('additionalConditions', '')
        try:
            delivery_infos = dct.get('deliveryInfos', [])[0].get('deliveryAddress', {})
            region_name = delivery_infos.get('regionName', '')
            delivery_info = f'{delivery_infos.get("city", "")} {delivery_infos.get("street", "")} {delivery_infos.get("house", "")}'
        except IndexError:
            delivery_info = ''
            region_name = ''
        lotsitems = []
        try:
            ok_lots = dct.get('lotItems', [])
            for lot in ok_lots:
                temp_dct = {}
                temp_dct['name'] = f'{lot.get("eat", {{}}).get("title", "")}. {lot.get("okpd2", {{}}).get("title", "")}'
                temp_dct['count'] = lot.get('quantity', '')
                temp_dct['unit'] = lot.get('okei', {}).get('title', '')
                temp_dct['unit_price'] = lot.get("unitPrice")
                temp_dct['cost'] = lot.get('sum', '')
                lotsitems.append(temp_dct)
        except Exception as ex:
            pass

        nice_dct = {'lots': [{"region": region_name, "deliveryPlace": delivery_info, "additionalInfo": addt_info,
                              "lotItems": lotsitems}]}

        return nice_dct

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
        dct = dct.get('trade',{}).get('lots',{})
        type = dct.get('deliveryType')

        match type:
            case 1 if dct.get("deliveryPeriod",''):
                return f"{dct.get('deliveryPeriod','')} рабочих дня от даты заключения контракта"
            case 2 if dct.get("deliveryDate",''):
                formated_data = datetime.strptime(dct.get("deliveryDate"), '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y')
                return formated_data
            case _:
                return ''

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
