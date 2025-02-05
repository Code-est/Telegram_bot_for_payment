# Класс History предоставляет информацию о 100 последних операциях на аккаунте

import requests

class History():

    def all_history(self):

        url = "https://yoomoney.ru/api/operation-history"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization" : "Bearer ",
            "Content-Length" : "9"
        }

        data = {

            "records" : "100"
        }

        # Выполнение запроса
        response = requests.post(url, headers=headers, data=data)

        # Обработка ответа
        if response.status_code == 200:
            #print("Успех:", response.status_code, response.text+",")
            return (response.text+",")
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
