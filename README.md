# Запуск

 - Клонируем на устройство: `bash git clone https://github.com/anniemcfly/0g-faucet-script.git`
 - Заходим в папку: `bash cd 0g-faucet-script`
 - Создаём виртуальное окружение: `bash python3 -m venv venv` и заходим в него `bash source venv/bin/activate`
 - Устанавливаем библиотеки из файла: `pip install -r requirements.txt`
 - Создаём файл `bash .env` и вносим в него три переменные: `bash RU_CAPTCHA_API_TOKEN`, `bash SITE_KEY_HCAPTCHA`, `bash SITE_KEY_HCAPTCHA` `bash SOFT_ID`. Последняя должна быть равна 0.
 - Генерируем кошельки `bash python3 src/evm_wallets.py`
 - Запускаем скрипт `bash python3 main.py`

Далее просто жмём три раза enter. Как только все кошельки получат баланс скрипт остановится и будет ждать 24 часа.
