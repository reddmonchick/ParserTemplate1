import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

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
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            stealth_sync(page)
            page.goto('https://www.coingecko.com/')
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

        json_data['page'] = page_num
        url = 'https://tender-cache-api.agregatoreat.ru/api/TradeLot/list-published-trade-lots'
        response = requests.post(url=url,headers=headers,json_data=json_data)
        if response.status_code == 200:
            json_items = []
            json_ = response.json()
            for dct in json_:
                id = dct.get('id')
                card_response = requests.get('https://tender-cache-api.agregatoreat.ru/api/TradeLot/8b08852e-b904-45c7-8eeb-c1170a2a0dfd',headers=headers) # делаем запрос к карточке товара
                if card_response.status_code == 200:
                    json_items.append(dct,card_response.json())
                else:
                    break
            return json_items
        else:
            return []
        # собираем все ссылки и возвращаем итерируемый объект, желательно tuple
