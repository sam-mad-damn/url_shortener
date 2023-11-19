
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
    if cursor.execute('''SELECT id FROM users WHERE login=?;''', ([login,])).fetchone() != None:
        return True
    else:
        return False

def get_user_id(cursor,login):
    return cursor.execute('''SELECT id FROM users WHERE login=?;''', ([login,])).fetchone()

#функция добавления ссылки
def add_link(connection, long, access_lvl, shortname, short, count=0, user_id=0):
    if find_link_by_shortname(connection,shortname)==None:
        access_lvl_name=find_access_lvl(connection,access_lvl)[0]
        connection.cursor().execute('''INSERT INTO links(long,shortname,short,count,user_id,access_lvl, access_lvl_name) VALUES(?,?,?,?,?,?,?)''',([long, shortname, short, count, user_id, access_lvl,access_lvl_name,]))
        connection.commit()
        return find_link_by_short(connection,short,user_id)
    else:
        return False

#функция удаление ссылки
def del_link(connection, id):
    connection.cursor().execute('''DELETE FROM links WHERE id=?''',([id,]))
    connection.commit()

#функция изменения количества переходов ссылки
def change_count_link(connection, count, id):
    connection.cursor().execute('''UPDATE links SET count =? WHERE id=?''',([count,id,]))
    connection.commit()

def change_access_lvl_link(connection, access_lvl, id):
    access_lvl_name = find_access_lvl(connection,access_lvl)[0]
    connection.cursor().execute('''UPDATE links SET access_lvl=?,access_lvl_name=? WHERE id=?''',([access_lvl, access_lvl_name, id,]))
    connection.commit()

def change_shortname_link(connection, shortname, short, id):
    connection.cursor().execute('''UPDATE links SET shortname =?, short=? WHERE id=?''',([shortname,short,id,]))
    connection.commit()

#функция поиска ссылки
def find_link_by_short(connection, short, user_id):
     return connection.cursor().execute('''SELECT * FROM links WHERE short=? AND user_id=?''',
                                          ([short,user_id,])).fetchone()
#функция поиска ссылки
def find_link_by_shortname(connection, short):
     return connection.cursor().execute('''SELECT * FROM links WHERE shortname=? ''',
                                          ([short,])).fetchone()


def find_link_by_long(connection, long, user_id):
    return connection.cursor().execute('''SELECT * FROM links WHERE long=? AND user_id=? ''',
                                       ([long,user_id, ])).fetchone()
#функция поиска ссылки
def find_link_by_id(connection, link_id):
     return connection.cursor().execute('''SELECT * FROM links WHERE id=?''',
                                          ([link_id,])).fetchone()

# функция получения списка ссылок пользователя
def get_users_links(cursor,user_id):
    return cursor.execute('''SELECT * FROM links WHERE user_id=?;''',([user_id])).fetchall()

def get_access_lvls(connection):
    return connection.cursor().execute('''SELECT * FROM access_lvl''').fetchall()

def find_access_lvl(connection, lvl):
    return connection.cursor().execute('''SELECT description FROM access_lvl WHERE lvl=?''',[lvl,]).fetchone()