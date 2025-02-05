import requests


url = "https://yoomoney.ru/api/account-info"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization" : "Bearer "
}

data = {
	
	"param1" : "value1",
	"param2" : "value2",
	"param3" : "value3"
}

# Выполнение запроса
response = requests.post(url, headers=headers, data=data)

# Обработка ответа
if response.status_code == 200:
    print("Успех:", response.status_code, response.text)
else:
    print(f"Ошибка {response.status_code}: {response.text}")
