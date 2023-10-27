
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

# функция получения id пользователя
def find_user(cursor, login, password):
    if cursor.execute('''SELECT id FROM users WHERE login=? AND password=?;''', ([login,password,])).fetchone() != None:
        return True
    else:
        return False

def get_user_id(cursor,login):
    return cursor.execute('''SELECT id FROM users WHERE login=?;''', ([login,])).fetchone()

#функция добавления ссылки
def add_link(connection, long, short, count=0):
    connection.cursor().execute('''INSERT INTO links(long,short,count) VALUES(?,?,?)''',([long, short, count]))
    connection.commit()
    connection.close()

# функция добавления ссылки пользователя
def add_user_link(connection, user_id, link_id, access_lvl):
    connection.cursor().execute('''INSERT INTO users_links(user_id,link_id,access_lvl) VALUES(?,?,?)''',
                                ([user_id, link_id, access_lvl]))
    connection.commit()
    connection.close()


# функция получения списка ссылок пользователя
def get_users_links(cursor,user_id):
    cursor.execute('''SELECT * FROM links WHERE links.id=users_links.link_id AND users_links.user_id=?;''',([user_id])).fetchall()