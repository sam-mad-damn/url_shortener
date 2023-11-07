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
    '''CREATE TABLE IF NOT EXISTS "links"(id INTEGER PRIMARY KEY AUTOINCREMENT,long TEXT NOT NULL, shortname TEXT NOT NULL, short TEXT NOT NULL, count INT NOT NULL, user_id TEXT NOT NULL, access_lvl INT NOT NULL, access_lvl_name TEXT NOT NULL);''')
# cursor.execute('''DROP TABLE links''')
# создаем таблицу уровни доступа в базе, если она еще не существует
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS "access_lvl"(id INTEGER PRIMARY KEY AUTOINCREMENT,lvl INTEGER NOT NULL, description TEXT NOT NULL);''')
# проверяем если таблица пустая то заполняем её
if(cursor.execute('''SELECT * FROM access_lvl''').fetchall() == []):
    for k,v in access_lvls.items():
        cursor.execute('''INSERT INTO access_lvl(lvl,description) VALUES(?,?)''',([k,v]))

# зафиксировали изменения в базе
con.commit()
# закрыли подключение
con.close()