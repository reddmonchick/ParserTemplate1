import os

import requests
from loguru import logger
import settings


if settings.PRODUCTION:
    from Send_report.mywrapper import magicDB
    logger.debug("production TRUE, SENDING DATA")
else:
    logger.debug("production FALSE, PRINT DATA")
    def magicDB(func):
        def wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            check_data_through_validator(result)
            return result
        return wrap


def send_to_core(result_data: dict) -> dict:
    if isinstance(result_data['data'], list):
        logger.debug(f'send to core input data count: {len(result_data.get("data"))} elements')
    elif isinstance(result_data['data'], str):
        logger.critical(f"ERROR PARSING, MSG: {result_data.get('msg')}")
    return result_data


def check_data_through_validator(result: dict) -> None:
    url = os.getenv("VALIDATOR_URL")
    response = requests.post(url=url, json=result, headers={'Content-Type': 'application/json'})
    if response.status_code in (200, 201):
        logger.info(f"response -> {response.json()}")
    else:
        logger.error(f"response status code: {response.status_code},\n"
                     f"body: {response.json()}")

