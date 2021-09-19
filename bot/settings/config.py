from dotenv import load_dotenv
import os

load_dotenv()  

IP_BACKEND = "127.0.0.1"
PORT_BACKEND = "8000"

API_TOKEN = "os.environ.get('BOT_TOKEN')"
API_ORDERS = f"http://{IP_BACKEND}:{PORT_BACKEND}/api/orders/"
API_DOCTORS = f"http://{IP_BACKEND}:{PORT_BACKEND}/api/doctors/"

API_ORDER = f"http://{IP_BACKEND}:{PORT_BACKEND}/api/orders/"

API_DOCTOR_SEARCH = f"http://{IP_BACKEND}:{PORT_BACKEND}/api/doctors/?search="

keyboard = {
    "create": "Создать заявку"
}

group_id = "-576430577"

rights = """
Добро пожаловать!

Для регистрации в системе введите команду: /register

Обработка заявок:
Заявка приходит к Вам в чат с кнопками "Принять" и "Отменить"

1) Если Вы не можете обработать заявку: нажмите "Отменить"
2) Если Вы готовы обработать заявку: нажмите "Принять". После чего заявка примет статус обработки и появятся две кнопки "Выполнить" и "Отменить".
Нажмите "Выполнить", когда Вы выполнили задачу.
Если не получается выполнить, то нажмите "Отменить" и введите причину.
"""
