import requests


url = "https://yoomoney.ru/oauth/authorize"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Параметры запроса
data = {
    "client_id" : "",
    "response_type" : "code",
    "redirect_uri": "http://site.ru",
    "scope" : "account-info operation-history operation-details"
}

# Выполнение запроса
response = requests.post(url, headers=headers, data=data)

# Обработка ответа
if response.status_code == 200:
    print("Успех:", response.status_code, response.text)
else:
    print(f"Ошибка {response.status_code}: {response.text}")
    