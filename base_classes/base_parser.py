import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from loguru import logger
import time



class BaseParser:

    def get_tender_links_from_page(self, page_num: int) -> tuple:
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': 'Bearer null',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://agregatoreat.ru',
            'Pragma': 'no-cache',
            'Referer': 'https://agregatoreat.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'page': 1,
            'size': 100,
            'isReviewAwaiting': False,
            'isCustomerSendingAwaiting': False,
            'isCustomerSigningAwaiting': False,
            'isSupplierSigningAwaiting': False,
            'isChangeDealTermsProtocolReceived': False,
            'isWinner': False,
            'isLoser': False,
            'searchText': '',
            'purchaseName': '',
            'number': None,
            'lotItemEatCodes': [],
            'productCode': None,
            'okpd2Codes': [],
            'ktruCodes': [],
            'purchaseTypeIds': [],
            'types': [],
            'customerId': None,
            'customerNameOrInn': None,
            'customerInn': None,
            'customerKpp': None,
            'supplierNameOrInn': None,
            'purchaseMethods': [],
            'priceStart': None,
            'priceEnd': None,
            'deliveryAddressRegionCodes': [],
            'deliveryAddress': None,
            'contractPriceStart': None,
            'contractPriceEnd': None,
            'applicationFillingStartDate': None,
            'applicationFillingEndDate': None,
            'contractSignDateStart': None,
            'contractSignDateEnd': None,
            'deliveryDateStart': None,
            'deliveryDateEnd': None,
            'isSmpOnly': False,
            'isEatOnly': False,
            'stateDefenseOrderOnly': None,
            'createDateTime': None,
            'excludeCancelledByCustomer': False,
            'excludeExternalTrades': False,
            'publishDateBegin': None,
            'publishDateEnd': None,
            'updateDateBegin': None,
            'updateDateEnd': None,
            'applicationFillingStartDateBegin': None,
            'applicationFillingStartDateEnd': None,
            'customerContractNumber': None,
            'hasLinkedExternalTrade': None,
            'eisTradeNumber': None,
            'isSpecificSupplier': False,
            'isRussianItemsPurchase': None,
            'organizerRegions': [],
            'organizerRegion': None,
            'lotStates': [
                2,
            ],
            'sort': [
                {
                    'fieldName': 'publishDate',
                    'direction': 2,
                },
            ],
        }
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            stealth_sync(page)
            page.goto('https://agregatoreat.ru/purchases/new')
            time.sleep(3)
            cookies = page.context.cookies()
            browser.close()
        def cookies_to_dict(cookies):
            cookies_dict = {}
            for cookie in cookies:
                cookies_dict[cookie["name"]] = cookie["value"]
            return cookies_dict


        cookies = cookies_to_dict(cookies)
        print(cookies)
        c = 0
        json_data['page'] = page_num
        url = 'https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots'
        response = requests.post(url=url,headers=headers,json=json_data)
        if response.status_code == 200:
            logger.info('Успешно получили 100 карточек')
            json_items = []
            json_ = response.json().get('items')
            for dct in json_:
                id_ = dct.get('id')
                logger.debug(f'Делаем запрос на ссылку https://tender-cache-api.agregatoreat.ru/api/TradeLot/{id_}')
                card_response = requests.get(f'https://tender-cache-api.agregatoreat.ru/api/TradeLot/{id_}',headers=headers) # делаем запрос к карточке товара
                if card_response.status_code == 200:
                    c += 1
                    logger.debug(f'Успешно {c}/100')
                    json_items.append((dct,card_response.json()))
                else:
                    break
            logger.debug(f'Отправляем в парсер на обработку кол карточек: {len(json_items)}')
            return json_items
        else:
            return []
        # собираем все ссылки и возвращаем итерируемый объект, желательно tuple
