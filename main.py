from flask import Flask, request, redirect, jsonify, render_template,  flash, session
from bd import *
import os
from functions import *
# from flask_login import LoginManager, login_user, current_user, logout_user
# from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import sqlite3, uuid,  random
from flask_bcrypt import Bcrypt

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
                session["auth"] = True
                # отправляем на страницу профиля
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
            session["auth"]=True
            # переносим на страницу профиля
            return redirect(f'http://127.0.0.1:5000/profile')
        # если уже зареган то
        else:
            session["auth"]=False
            # остаемся на странице регистрации
            return render_template('register.html', auth=False)
    return render_template('register.html')

@app.route('/profile')
def profile():
    if "auth" in session:
        return render_template("profile.html", auth=session["auth"])
    else:
        return redirect(f'http://127.0.0.1:5000/login')

@app.route('/logout')
def logout():
    session.pop('auth', None)
    return redirect(f"http://127.0.0.1:5000/")

if __name__ == '__main__':
    app.run(debug=True)

