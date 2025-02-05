from history import History
from info_2 import Info

import sqlite3
import time
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import FSInputFile


# Настройки. Не трогать
#################################################################################
con = sqlite3.connect("data.db", check_same_thread=False)                       #
cur = con.cursor()                                                              #
#################################################################################
TOKEN = " "                        #
dp = Dispatcher()                                                               #
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) #
#################################################################################
log_list = {}                                                                   #
#################################################################################


# Вспомогательные функции
###########################################################################################################################
def the_amount_info(user_id):
    return str(cur.execute(f"SELECT The_amount FROM users_and_payments WHERE Telegram_client_ID = '{user_id}'").fetchall())

def filter_text(filt):
    nums = "[", "]", "(", ")", "'", ","
    amount_filter = []
    for i in str(filt):
        if i not in nums:
            amount_filter.append(i)
    return "".join(amount_filter)

async def photo(amount, id):
    print(float(amount), "DA")
    if float(amount) >= 0.02:
        img = FSInputFile("cat.jpg")
        await bot.send_photo(chat_id= id, photo=img, caption = "Спасибо за оплату! Вот ваша картинка")

async def cooldown():
    while True:
        await asyncio.sleep(60)
        log_list.clear()
        print("log_list очищен")

def add_user_and_time(usr1):
    log_list[usr1] = time.time()
    print(f"В log list добавлен пользователь {usr1} с со временем " + str(log_list[usr1]))

def user_check(usr):
    if usr in log_list:
        if time.time() - log_list[usr] > 5:
            return 0
        else:
            print(f"Слишком частый запрос от пользователя {usr}")
            return 1
    else:
        return 0
###########################################################################################################################


# Основные функции бота
###########################################################################################################################
@dp.message(CommandStart())
async def start(message: Message):
    user_id = int(message.from_user.id)
    if user_check(user_id) == 0:
        add_user_and_time(user_id)
        if f'({user_id},)' not in str(cur.execute("SELECT Telegram_client_ID FROM users_and_payments").fetchall()):
            cur.execute(f'INSERT INTO users_and_payments VALUES ("", "{user_id}", "", "", 0.00)')
            con.commit()
            print(f"Новый ID {user_id} добавлен в базу")
        await message.answer(f"Здравствуйте, для получения картинки отправьте перевод на счет 410011813133047 в Юмани по СБП через любой удобный банк."
                                          f"\nСумма перевода должна составлять 0,02 руб. После перевода просто напишите в чат Идентификатор перевода СБП, который присваивается каждому переводу."
                                          f"\n\n Сейчас ваш балланс составляет: {filter_text(the_amount_info(user_id))} / 0,02 руб."
                             )
        await photo(filter_text(the_amount_info(message.from_user.id)), message.chat.id)

@dp.message()
async def text_code(message: Message):
    user_id = int(message.from_user.id)
    if user_check(user_id) == 0:
        add_user_and_time(user_id)
        injection = 0
        for i in open("injections.txt", "r"):
            if i.replace("\n","") in message.text.upper():
                print("SQL-инъекция")
                injection = 1
                break
        if injection == 0:
                Info().information(History().all_history())
                if f"('{message.text}',)" in str(cur.execute("SELECT Transfer_ID FROM payments").fetchall()):
                    if "in" in str(cur.execute(f"SELECT In_out FROM payments WHERE Transfer_ID = '{message.text}'").fetchall()):
                        if "[('Yes',)]" not in str(cur.execute(f"SELECT Use FROM payments WHERE Transfer_ID = '{message.text}'").fetchall()):
                                print((cur.execute(f"SELECT Use FROM payments WHERE Transfer_ID = '{message.text}'").fetchall()))
                                cur.execute(f'UPDATE payments SET Use = "Yes" WHERE Transfer_ID = "{message.text}"')
                                con.commit()
                                amount_1 = float(filter_text(cur.execute(f"SELECT The_amount FROM users_and_payments WHERE Telegram_client_ID = '{message.from_user.id}'").fetchall()))
                                amount_2 = float(filter_text(cur.execute(f'SELECT The_amount FROM payments WHERE Transfer_ID = "{message.text}"').fetchone()))
                                amount_sum = amount_1 + amount_2
                                cur.execute(f'UPDATE users_and_payments SET The_amount = "{amount_sum}", Transfer_ID = "\n{message.text}" WHERE Telegram_client_ID = "{message.from_user.id}"')
                                con.commit()
                                await message.answer(f"Спасибо, теперь ваш балланс составляет: {filter_text(the_amount_info(message.from_user.id))} / 0.02 руб.")
                                await photo(filter_text(the_amount_info(message.from_user.id)), message.chat.id)
                        else:
                            print(f"Код {message.text} существует в базе, но параметры In_out или Use не прошли проверку")
                else:
                    print(f"Кода {message.text} не существует в базе")
        else:
            injection = 0
###########################################################################################################################


# Функции для запуска. Не трогать
###########################################################################################################################
async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    task1 = asyncio.create_task(cooldown())
    task2 = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())