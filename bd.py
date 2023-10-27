# импортируем библиотеку для работы с базой данных
import sqlite3
from config import *
from functions import *

# создали подключение к бд. если такой базы нет, то она создастся сама
con = sqlite3.connect(r"db.db")
# создали курсор для запросов
cursor = con.cursor()
# создали таблицу users в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER NOT NULL,"login" TEXT NOT NULL,"password" TEXT NOT NULL,primary key("id" AUTOINCREMENT));''')
# cursor.execute('''DROP TABLE users''')

# создаем таблицу links в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "links"(id INTEGER PRIMARY KEY AUTOINCREMENT,long TEXT NOT NULL, short TEXT NOT NULL, count INT NOT NULL);''')

# создаем таблицу уровни доступа в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "access_lvl"(id INTEGER PRIMARY KEY AUTOINCREMENT,lvl INTEGER NOT NULL, description TEXT NOT NULL);''')
# проверяем если таблица пустая то заполняем её
if(cursor.execute('''SELECT * FROM access_lvl''').fetchall() == []):
    for k,v in access_lvls.items():
        cursor.execute('''INSERT INTO access_lvl(lvl,description) VALUES(?,?)''',([k,v]))

# создаем таблицу users_links в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "users_links"(user_id INTEGER NOT NULL, link_id INTEGER NOT NULL, access_lvl INTEGER NOT NULL);''')

# зафиксировали изменения в базе
con.commit()
# закрыли подключение
con.close()