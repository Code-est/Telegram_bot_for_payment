# Класс Info предоставляет информацию: номер операции, приход или уход, сумму, время операции

import requests
import sqlite3
from history import History
from details import Details
import time

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()

class Info():

	def information(self, history):
		b = []
		c = []

		for i in history:
			b.append(i)
			if b[-1] == "," and b[-2] == "}":
				c.append("".join(b))
				b.clear()

		for i in c:
			#print(i)
			operation_id = i[i.find('","operation_id":"')+len('","operation_id":"') : i.rfind('","title":"')]
			in_out = i[i.find('"direction":"')+len('"direction":"') : i.rfind('","datetime"')]
			the_amount = i[i.find('"sum":')+len('"sum":') : i.rfind('}],"amount')]
			date_time = i[i.find('"datetime":"')+len('"datetime":"') : i.rfind('Z","status"')].replace("T", " ")

			if f'({operation_id},)' not in str(cur.execute("SELECT Operation_ID FROM payments").fetchall()):


				if " платеж №" in Details().dtls(operation_id) and f'({operation_id},)':
					vstavka = Details().dtls(operation_id)[Details().dtls(operation_id).find(" платеж №")+len(" платеж №"):Details().dtls(operation_id).rfind('","gr')]
					cur.execute(f' INSERT INTO payments VALUES ("", "{vstavka}", "{in_out}", {the_amount}, {operation_id}, "{date_time}", "")')
					con.commit()
				else:
					cur.execute(f' INSERT INTO payments VALUES (1, "" , "{in_out}", {the_amount}, {operation_id}, "{date_time}", "") ')
					con.commit()

				print("Все добавлено")
				time.sleep(0.3)

		print("Проверка новых приходов выполнена")


Info().information(History().all_history())



