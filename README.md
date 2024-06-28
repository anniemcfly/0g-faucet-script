# Запуск

 - Клонируем на устройство: `git clone https://github.com/anniemcfly/0g-faucet-script.git`
 - Заходим в папку: `cd 0g-faucet-script`
 - Создаём виртуальное окружение: `python3 -m venv venv` и заходим в него `source venv/bin/activate`
 - Устанавливаем библиотеки из файла: `pip install -r requirements.txt`
 - Создаём файл `.env` и вносим в него три переменные: `RU_CAPTCHA_API_TOKEN`, `SITE_KEY_HCAPTCHA`, `SITE_KEY_HCAPTCHA` `SOFT_ID`. Последняя должна быть равна 0.
 - Генерируем кошельки `python3 src/evm_wallets.py`
 - Запускаем скрипт `python3 main.py`

Далее просто жмём три раза enter. Как только все кошельки получат баланс скрипт остановится и будет ждать 24 часа.
