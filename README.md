# Telegram_bot_for_payment

### Описание:
Телеграм бот, написанный на Python, созданный для продажи различных предметов.
#

### Принцип действия:
1. При самом первом запуске файла `main.py` и самой первой отправки команды `/start` код подгружает в базу данных файла `data.db` 100 последних операций с аккаунта Yoomoney.
2. После подгрузки базы в чате появляется сообщение с инструкцией по внесению денежных средств
3. В этот момент код заносит в базу уникальный номер телеграма пользователя в базу
4. Денежные средства переводятся с помощью Системы быстрых платежей по номеру телефона, указанный в инструкции
5. После перевода открываем чек по операции и копируем "Идентификатор операции в СПБ"
6. Вставляем Идентификатор операции в СПБ в чат
7. Код проверяет:
   * наличие Идентификатора операции в базе данных
   * что платеж имеет параметр "IN" (приход)
   * что платеж не использовался другим пользователем ранее
   * размер прихода
7. Далее код присваивает соответствующему пользователю размер прихода
8. Появляется картина с котиком и благодарностью за оплату
> [!NOTE]
> Если пользователь удалит чат и потом заново начнет переписку с ботом через команду `/start`, то бот снова отправит ему картинку с котиком, т.к. база данных хранит размер денежных средств на баллансе.
#

### Используемые технологии и API:
1. Библиотеки для Python: asyncio, sqlite3, aiogram (pip install aiogram)
2. SQL
3. Yoomoney API
#

### Особенности:
1. Программный код имеет кастомную защиту от SQL-инъекции, реализованную посредством проверки каждого сообщения на определенные слова/символы, позволяющие взаимодействовать с SQL таблицей. Список слов, на которые бот проверяет каждое сообщение хранятся в файле `injections.txt`.
3. Телеграм бот имеет защиту от спама, реализованную посредством запоминания времени последнего сообщения пользователя и сравнивания его с текущим временем. Этот параметр регулируется в настройках и по умолчанию равен "5".
4. Поскольку для осущствления функцианирования пункта 2 используется метод запоминания времени отправки последнего сообщения пользователем, то в коде предусмотрен бесконечный асинхронный цикл, который каждые 60 секунд очищает словарь с пользователями и временем. Внедрение данного цикла обуславливается необходимость в снижении нагрузки на бота.
5. Код данного бота полностью оптимизирован на многопользовательскую нагрузку.
> [!TIP]
> Если ожидается, что бот будет работать с очень большим количеством пользователей, то рекомендуется использовать соответствующие базы данных, поддерживающие многопоточное использование.
#

### Инструкция по запуску:

#
