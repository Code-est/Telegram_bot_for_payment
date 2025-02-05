# Класс * предоставляет подробную информацию о конкретной операции, в том числе и нужный номер идентификатора перевода СБП

import requests


class Details():

    def dtls(self, op):

        url = "https://yoomoney.ru/api/operation-details"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization" : "Bearer ",
            "Content-Length" : "20"
        }

        data = {

            "operation_id" : f"{op}"
        }

        # Выполнение запроса
        response = requests.post(url, headers=headers, data=data)

        # Обработка ответа
        if response.status_code == 200:
            #print("Успех:", response.status_code, response.text)
            return response.text
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
