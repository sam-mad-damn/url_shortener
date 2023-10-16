
# функция регистрации пользователя
def registration(connection, login, password):
    if find_user(connection.cursor(), login, password):
        return False
    else:
        add_user(connection, login, password)
        return True

#
def get_pass(cursor,login):
    password = cursor.execute('''SELECT password FROM users WHERE login=? ;''', ([login,])).fetchone()
    if password==None:
        return False
    else:
        return password
def authorization(cursor, login, password):
    user = cursor.execute('''SELECT password FROM users WHERE login=? ;''', ([login,])).fetchone()
    if user != None:
        if login==user[0] and password==user[1]:
            return True
    else:
        return False

# добавление пользователя в базу
def add_user(connection,login, password):
    connection.cursor().execute(
        '''INSERT INTO users(login,password) VALUES (?,?) ;''', ([login, password]))
    connection.commit()
    connection.close()

# функция получения id пользователя
def find_user(cursor, login, password):
    if cursor.execute('''SELECT id FROM users WHERE login=? AND password=?;''', ([login,password,])).fetchone() != None:
        return True
    else:
        return False

