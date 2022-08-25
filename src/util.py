from decimal import Decimal
import logging
import logging.handlers
import re

from conf import FOUNDATION_ADDR


class TipBotException(Exception):
    def __init__(self, error_type):
        self.error_type = error_type
        Exception.__init__(self)

    def __str__(self):
        return repr(self.error_type)


def find_amount(input_text):
    regex = r'(?:^|\s)(\d*\.?\d+)(?=$|\s)'
    matches = re.findall(regex, input_text, re.IGNORECASE)

    if len(matches) == 1:
        try:
            assert Decimal(matches[0]).as_tuple().exponent >= -6
            return float(matches[0].strip())

        except AssertionError:
            raise TipBotException("too_many_decimals")

    else:
        raise TipBotException("amount_not_found")


def find_address(input_text: str) -> str:

    # first check out if the tip goes to the foundation
    if "foundation" in input_text.lower():
        return FOUNDATION_ADDR

    # regex catching all kinds of Peercoin addreses
    regex = r'(?:(?:tpc|pc)(?:0(?:[ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})|(?:[Pp]|[mn2])[a-km-zA-HJ-NP-Z1-9]{25,39})'
    matches = re.findall(regex, input_text, re.IGNORECASE)
    if len(matches) == 1:
        return matches[0].strip()
    else:
        raise TipBotException("address_not_found")


def get_logger(name):
    formatter = logging.Formatter('%(asctime)s [%(name)s] -%(levelname)s- %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.handlers.TimedRotatingFileHandler('debug.log', when='midnight', backupCount=0)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger


def get_numerical_emoji(num):
    num_str = str(num)
    num_str = num_str.replace('0', ':zero:')
    num_str = num_str.replace('1', ':one:')
    num_str = num_str.replace('2', ':two:')
    num_str = num_str.replace('3', ':three:')
    num_str = num_str.replace('4', ':four:')
    num_str = num_str.replace('5', ':five:')
    num_str = num_str.replace('6', ':six:')
    num_str = num_str.replace('7', ':seven:')
    num_str = num_str.replace('8', ':eight:')
    num_str = num_str.replace('9', ':nine:')
    return num_str
