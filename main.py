from flask import Flask, request, redirect, jsonify, render_template,  flash, session
from bd import *
import os
from functions import *
import sqlite3, uuid,  random
from flask_bcrypt import Bcrypt
import hashlib

app = Flask(__name__, template_folder="templates", static_folder="templates/static")
# для хеширования паролей
bcrypt = Bcrypt(app)
# для работы с сессиями генерируем секретный код
Flask.secret_key=os.urandom(15)

@app.route('/')
def index():
    return render_template('index.html',auth=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            con=sqlite3.connect(r"db.db")
            # ловим введенные данные пользователя
            login = request.form['login']
            password = request.form['password']
            # берем из базы хэшированный пароль пользователя
            user_pass=get_pass(con.cursor(), login)
            # проверяем пароли и если совпадают то авторизуем пользователя
            if user_pass != False and bcrypt.check_password_hash(user_pass[0],password):
                authorization(con.cursor(), login, password)
                session["user_id"]=get_user_id(con.cursor(),login)[0]
                session["auth"] = True
                # отправляем на страницу профиля
                session["access_lvls"]=get_access_lvls(con)
                return redirect(f"http://127.0.0.1:5000/profile")
            # если не удалось авторизоваться, то
            else:
                return render_template('login.html', err="Не удалось войти. Неправильный логин или пароль")
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # подключаемся к базе данных
        con = sqlite3.connect(r"db.db")
        # ловим данные, которые ввел пользователь
        login = request.form['login']
        password = request.form['password']
        hashed_pass = bcrypt.generate_password_hash(password).decode("utf-8")
        # регистрируем пользователя, если он еще не зарегистрирован, то
        if registration(con, login, hashed_pass):
            session["user_id"] = get_user_id(con.cursor(), login)[0]
            session["auth"]=True
            # переносим на страницу профиля
            session["access_lvls"]=get_access_lvls(con)
            return redirect(f'http://127.0.0.1:5000/profile')
        # если уже зареган то
        else:
            session["auth"]=False
            # остаемся на странице регистрации
            return render_template('register.html', auth=False)
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if "auth" in session:
        con = sqlite3.connect(r"db.db")
        # get_users_links(con.cursor(), session["user_id"])
        if request.method == 'POST':
            if "del_link" in request.form:
                del_link(con, request.form["id_link"])
            elif "change_link" in request.form:
                session["finded_link"]=find_link_by_id(con, request.form["id_link"])
                print(session["finded_link"])
                return redirect(f"http://127.0.0.1:5000/change_link")
                # изменение кол-ва переходов
                # change_link(con, finded_link[4] + 1, request.form["id_link"])
            else:
                link = request.form['link']
                access_lvl = request.form['access_lvl']
                nickname = request.form['nickname']
                if nickname == "none":
                    shortname = hashlib.md5(link.encode()).hexdigest()[:random.randint(1,12)]
                    short=request.host_url+shortname
                else:
                    shortname = nickname
                    short=request.host_url+shortname
                added_link = add_link(con, link, access_lvl, shortname, short, user_id=session["user_id"])
                print(added_link)
        session["users_links"]=get_users_links(con.cursor(),session["user_id"])
        return render_template("profile.html", auth=session["auth"])
    else:
        return redirect(f'http://127.0.0.1:5000/login')

@app.route('/<short>')
def go(short):
    if "auth" in session:
        # подключаемся к базе данных
        con = sqlite3.connect(r"db.db")
        # ищем в базе ссылку по короткому имени
        finded_link=find_link_by_shortname(con,short,session["user_id"])
        if finded_link != None:
            change_count_link(con,finded_link[4]+1,finded_link[0])
        return redirect(finded_link[1])

@app.route('/change_link', methods=['GET', 'POST'])
def change_link():
    if "auth" in session:
        con = sqlite3.connect(r"db.db")
        if request.method == 'POST':
            link_id=session["finded_link"][0]
            if "del_nickname" in request.form:
                shortname = hashlib.md5(session["finded_link"][2].encode()).hexdigest()[:random.randint(1,12)]
                short = request.host_url + shortname
                change_shortname_link(con, shortname, short, link_id)
                return redirect(f'http://127.0.0.1:5000/profile')
            if "change_access_lvl" in request.form:
                access_lvl=request.form["access_lvl"]
                change_access_lvl_link(con,access_lvl,link_id)
                return redirect(f'http://127.0.0.1:5000/profile')
            if "change_nickname" in request.form:
                shortname=request.form["nickname"]
                short = request.host_url + shortname
                change_shortname_link(con,shortname,short,link_id)
                return redirect(f'http://127.0.0.1:5000/profile')
        return render_template("change_link.html")
    else:
        return redirect(f'http://127.0.0.1:5000/login')

@app.route('/logout')
def logout():
    session.pop('auth', None)
    return redirect(f"http://127.0.0.1:5000/")

if __name__ == '__main__':
    app.run(debug=True)

