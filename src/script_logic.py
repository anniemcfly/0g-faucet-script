import os
import re
import json
import time
import random

import requests
import openpyxl
from twocaptcha import TwoCaptcha, TimeoutException, ValidationException, NetworkException, ApiException
from dotenv import load_dotenv

from src.config import logger2

load_dotenv()


def random_user_agent(path_to_file: str = "src/user_agents.txt") -> tuple:
    """Возвращает случайный user_agent и платформу."""

    with open(path_to_file, "r") as file:
        content = file.read()

        user_agent = random.choice(content.split('\n'))
        match = re.search(r"\((\w+)", user_agent)
        platform = match.group(1)

        return user_agent, platform


def get_proxy(proxy_file: str) -> str:
    """Возвращает список прокси из файла."""

    if proxy_file == '':
        proxy_file = "src/proxy.txt"

    with open(proxy_file, 'r') as file:
        content = file.read()

    return content


def check_proxy_ip(proxy: str):
    """Проверяет какой ip адрес возвращает прокси сервер."""

    proxies = {
        'http': f'http://{proxy}'
    }

    response = requests.get('http://httpbin.org/ip', proxies=proxies)
    print(response.json())


def get_wallets(xlsx_w_wallets: str) -> list[str]:
    """Возвращает список из кошельков."""

    if xlsx_w_wallets == '':
        xlsx_w_wallets = 'src/new_wallets.xlsx'

    wallets_book = openpyxl.load_workbook(xlsx_w_wallets)
    actual_sheet = wallets_book.active

    wallets_list = []

    i = 2

    while True:
        cell_obj = actual_sheet.cell(row=i, column=1)

        if not cell_obj.value:
            logger2.debug("Кошельки закончились.")
            break

        wallets_list.append(cell_obj.value)
        logger2.debug(f"Кошелёк: {cell_obj.value} добавлен в список на пополнение.")

        i += 1

    logger2.info(f"Все кошельки были успешно получены из файла, длина массива: {len(wallets_list)}")
    return wallets_list


def touch_faucet(wallet: str, solver: TwoCaptcha, proxy: str | None = None) -> bool:
    """Пополняет баланс кошелька (Трогает кран)."""

    captcha_token = None

    try:
        captcha_token = solver.hcaptcha(sitekey=os.getenv("SITE_KEY_HCAPTCHA"), domain="js.hcaptcha.com",
                                        url="https://faucet.0g.ai", proxy={'type': 'HTTPS', 'uri': proxy})

        captcha_id = captcha_token['captchaId']

        while True:

            captcha_token = requests.get(f'https://2captcha.com/res.php?key={os.getenv("RU_CAPTCHA_API_TOKEN")}'
                                         f'&action=get&id={captcha_id}')

            if captcha_token.text == "CAPCHA_NOT_READY":
                time.sleep(5)
            else:
                break

    except TimeoutException:
        logger2.warning(f'Не удалось решить капчу! Прошло слишком времени.')
    except ValidationException:
        logger2.warning('Не получилось решить капчу! Проблема с передаваемыми данными.')
    except NetworkException:
        logger2.warning('Не удалось решить капчу! Проблема с интернет соединением.')
    except ApiException:
        logger2.warning('Не получилось пройти капчу! Проблема с API запросом.')

    post_data = {
        'address': wallet,
        'hcaptchaToken': captcha_token.text.split('|')[-1]
    }

    user_agent, platform = random_user_agent()

    headers = {
        'accept': '*/*',
        'accept-language': 'ko',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://faucet.0g.ai',
        'priority': 'u=1, i',
        'sec-ch-ua-mobile': '?0',
        'referer': 'https://faucet.0g.ai/',
        'sec-ch-ua-platform': f'"{platform}"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': f'{user_agent}',
    }

    check_proxy_ip(proxy)

    if proxy:
        proxy = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    print(proxy)

    response = requests.post(url="https://faucet.0g.ai/api/faucet", data=json.dumps(post_data),
                             headers=headers, proxies=proxy)

    if response.status_code != 200:
        logger2.warning(f'Не получилось пополнить баланс кошелька: {wallet} - Ответ от сервера: {response.text}')
        return False

    logger2.info(f'Баланс кошелька: {wallet} был успешно пополнен!')
    return True
