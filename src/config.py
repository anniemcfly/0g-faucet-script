"""
    Файл конфигурации.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)

handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler2.setFormatter(formatter2)
logger2.addHandler(handler2)
logger2.addHandler(logging.StreamHandler())


solver_config: dict = {
    'server': '2captcha.com',
    'apiKey': os.getenv("RU_CAPTCHA_API_TOKEN"),
    'softId': os.getenv("SOFT_ID"),
    'defaultTimeout': 120,
    'recaptchaTimeout': 600,
}

SLEEP_TIME = 1
SLEEP_TIME_SALT_SECONDS = [3, 4, 1, 5, 8, 10, 11, 22, 12, 13, 2]
