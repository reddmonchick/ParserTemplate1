# -*- coding: utf-8 -*-
import settings
import traceback
from base_classes.Send_data import send_to_core
from loguru import logger
from datetime import datetime
from Parser import Parser
logger.add("parser.log")


if __name__ == "__main__":
    start_time = datetime.now()
    parser_name = "PARSER_NAME"  # todo: согласно ТЗ
    parser = Parser(
        parser_name=parser_name
    )

    try:
        parser.run()

        # если был открыт веб драйвер, то нужно его закрыть
        # parser.driver.close()
        
        finish_time = datetime.now()
        logger.info(f"Парсер отработал за {finish_time - start_time}")
        exit(0)

    except Exception as err:
        # если был открыт веб драйвер, то нужно его закрыть
        # parser.driver.close()
        msg = str(traceback.format_exc())
        finish_time = datetime.now()
        logger.error(f"Парсер упал с ошибкой: {msg}")
        logger.info(f"Парсер отработал до ошибки за время {finish_time - start_time}")
        send_to_core({
            'name': parser_name,
            'data': 'error',
            'msg': msg
        })
        exit(1)
