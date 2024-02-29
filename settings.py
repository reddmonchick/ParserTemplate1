import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PRODUCTION = False
if PRODUCTION:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    base_path = os.path.dirname(current_dir)
    sys.path.append(base_path)
    sys.path.append("/home/manage_report")
    dotenv_path = Path("/home/service/.env")

else:
    dotenv_path = Path('.env')

load_dotenv(dotenv_path=dotenv_path)
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH")

# прокси
PROXIES = {
    "http": os.getenv("PROXIES_HTTP"),
    "https": os.getenv("PROXIES_HTTPS"),
}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
}

DEFAULT_STOP_ID = "https://tender.samolet.ru/trades/118718951/info"


