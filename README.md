# Тестовое задание SimbirSoft

Установка окружения и запуск теста (Python3.12, venv):

- pip install -r requirements.txt
- pytest --alluredir=./reports banking_test.py

Запуск Allure

- allure serve ./reports

Директории csv и reports не добавлял в .gitignore нарочно :)
Selenoid развернут на моей VPS и доступен по указанному в конфиге IP.
Selenoid UI доступен по http://185.93.109.120:8080/#/.