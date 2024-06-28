import time
import random

from twocaptcha import TwoCaptcha

from src import config
from src.config import logger2
from src.script_logic import get_wallets, get_proxy, touch_faucet

path_to_proxy_file = str(input("Введите пути до файла с прокси (Опционально): "))
sleep_time = input("Введите интервал между запросами в минутах (Опционально): ")
path_to_wallets_list = str(input("Укажите путь до файла с кошельками (Опционально): "))


wallets_list = get_wallets(xlsx_w_wallets=path_to_proxy_file)
proxy = get_proxy(proxy_file=path_to_proxy_file)

if not sleep_time:
    sleep_time = config.SLEEP_TIME
    logger2.info(f"Был установлен стандартный интервал: {sleep_time} мин.")

solver = TwoCaptcha(**config.solver_config)

last_wallet = ''

while True:
    for wallet in wallets_list:
        logger2.info(f"Пополняется кошелёк: {wallet}")

        response = touch_faucet(wallet, solver, proxy)

        if response:
            logger2.info("Кошелёк был успешно пополнен!")

        sleep_time = sleep_time*60+random.choice(config.SLEEP_TIME_SALT_SECONDS)
        logger2.info(f"Пауза: {sleep_time/60} мин.")
        time.sleep(sleep_time)

        sleep_time = config.SLEEP_TIME

    time.sleep(86400+30)    # После того как тронули все кошельки ждём 24 часа и повторяем.
