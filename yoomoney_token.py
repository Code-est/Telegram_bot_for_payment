import requests


url = "https://yoomoney.ru/oauth/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Параметры запроса
data = {
    "code" : " ",
    "client_id" : " ",
    "grant_type": "authorization_code",
    "redirect_uri": "http://site.ru"
}

# Выполнение запроса
response = requests.post(url, headers=headers, data=data)

# Обработка ответа
if response.status_code == 200:
    print("Успех:", response.status_code, response.text)
else:
    print(f"Ошибка {response.status_code}: {response.text}")
    