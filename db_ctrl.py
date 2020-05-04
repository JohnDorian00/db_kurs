import pyodbc
import logging.config
import os
from user import User, hash_password
from tkinter import messagebox

logging.config.fileConfig("conf/logging.conf")
log = logging.getLogger("db_ctrl")

print("db path:" + os.getcwd() + "\\data.accdb")


def connect_db():
    try:
        path = os.getcwd() + "\\data.accdb"
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                              r'*.accdb)};DBQ=' + path + ';')
        return conn.cursor()
    except pyodbc.Error as e:
        log.error("Ошибка подключения к базе данных" + ", err = " + ' '.join(str(e).split()))
        messagebox.showerror("Неудача", "Ошибка подключения к базе данных")
        return None


def get_user(login):
    login = str(login)
    cursor = connect_db()
    if cursor is None:
        return

    if login != "":
        sql = "SELECT * FROM users WHERE login = '" + login + "'"
        print("Выбран пользователь " + login)
    else:
        log.info("Не введен логин")
        cursor.close()
        return User()
    cursor.execute(sql)
    u = cursor.fetchone()
    cursor.close()

    if u is not None:
        return User(u[0], u[1], u[2], u[3])
    else:
        log.info("Попытка поиска пользователя с несуществующим логином - " + login)
        return User()


def get_all_users():
    cursor = connect_db()
    if cursor is None:
        return
    try:
        cursor.execute("SELECT * FROM users")
    except Exception as e:
        log.error("Ошибка чтения базы данных пользователей" + ", err = " + ' '.join(str(e).split()))
        cursor.close()
        return None
    d = cursor.fetchall()
    cursor.close()
    return d


def add_user(user):
    cursor = connect_db()
    if cursor is None:
        return
    try:
        cursor.execute("INSERT INTO users ( login, pass_hash, user_type ) VALUES ( ?, ?, ?)",
                       (user.login, hash_password(user.pass_hash), user.user_type))
        cursor.commit()
        log.info("Добавлен пользователь " + user.login + " c правами " + user.user_type)
    except Exception as e:
        log.error("Ошибка добавления пользователя" + ", err = " + ' '.join(str(e).split()))
    cursor.close()


def del_user(login):
    login = str(login)
    cursor = connect_db()
    if cursor is None:
        return
    try:
        cursor.execute("DELETE FROM users WHERE login = ?", login)
        cursor.commit()
        log.info("Пользователь " + login + " удален")
    except Exception as e:
        log.error("Ошибка удаления пользователя" + ", err = " + ' '.join(str(e).split()))
    cursor.close()


def get_seller(login):
    login = str(login)
    cursor = connect_db()
    if cursor is None:
        return
    if login:
        cursor.execute("SELECT * FROM sellers WHERE login = ?", login)
        print("Выбран продавец " + login)
    else:
        log.info("Не введен логин продавца")
        cursor.close()
        return
    s = cursor.fetchone()

    if s is not None:
        cursor.close()
        return s
    else:
        log.info("Попытка поиска продавца с несуществующим логином - " + login)
        cursor.close()
        return None


def get_all_sellers(city=None):
    cursor = connect_db()
    if cursor is None:
        return
    try:
        if city is None:
            cursor.execute("SELECT * FROM sellers")
        else:
            cursor.execute("SELECT * FROM sellers WHERE city = ?", city)
            print("Выбраны все продавцы по городу " + city)
    except Exception as e:
        log.error("Ошибка чтения базы данных продавцов" + ", err = " + ' '.join(str(e).split()))
        cursor.close()
        return None
    d = cursor.fetchall()
    cursor.close()
    return d


def update_seller(login, fio, city, avg_price):
    login = str(login)
    avg_price = str(avg_price)
    cursor = connect_db()
    if cursor is None:
        return

    s = get_seller(login)
    if s is None:
        cursor.execute("INSERT INTO sellers (login) VALUES (?)", login)
        cursor.commit()
        print("Продавец " + login + "записан в базу данных")
        s = get_seller(login)

    if fio == "":
        fio = s[2]
    if city == "":
        city = s[3]
    if avg_price == "":
        avg_price = s[4]
    cursor.execute("UPDATE sellers SET FIO = ?, city = ?, avg_price = ? WHERE ID = ?", fio, city, avg_price, s[0])
    cursor.commit()
    log.info("Обновлен продавец " + s[1])
    cursor.close()


def get_buyer(login):
    login = str(login)
    cursor = connect_db()
    if cursor is None:
        return
    cursor.execute("SELECT * FROM buyers WHERE login = ?", login)
    print("Выбран покупатель " + login)
    s = cursor.fetchone()

    if s is not None:
        cursor.close()
        return s
    else:
        log.info("Попытка поиска покупателя с несуществующим логином - " + login)
        cursor.close()
        return None


def update_buyer(login, fio, city):
    login = str(login)
    cursor = connect_db()
    if cursor is None:
        return

    b = get_buyer(login)
    if b is None:
        cursor.execute("INSERT INTO buyers (login) VALUES (?)", login)
        cursor.commit()
        b = get_buyer(login)

    if fio == "":
        fio = b[2]
    if city == "":
        city = b[3]
    cursor.execute("UPDATE buyers SET FIO = ?, city = ? WHERE ID = ?", fio, city, b[0])
    cursor.commit()
    log.info("Обновлен покупатель " + b[1])
    cursor.close()


def get_fav_list(buyer_login):
    buyer_login = str(buyer_login)
    cursor = connect_db()
    if cursor is None:
        return

    cursor.execute("SELECT * FROM fav_sellers WHERE buyer_login = ?", buyer_login)
    fav_list_all = cursor.fetchall()
    fav_list = []
    for v in fav_list_all:
        fav_list.append(v[2])
    cursor.close()
    return fav_list


def add_fav_seller(buyer_login, seller_login):
    buyer_login = str(buyer_login)
    seller_login = str(seller_login)
    cursor = connect_db()
    if cursor is None:
        return

    if get_buyer(buyer_login) is None:
        cursor.execute("INSERT INTO buyers (login) VALUES (?)", buyer_login)
        cursor.commit()

    cursor.execute("SELECT * FROM fav_sellers WHERE buyer_login = ? and seller_login = ?", buyer_login, seller_login)
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO fav_sellers ( buyer_login, seller_login) VALUES (?, ?)",
                       (buyer_login, seller_login))
        cursor.commit()
        log.info("Продавец " + seller_login + " добавлен в список избранных покупателя " + buyer_login)
        cursor.close()
    else:
        log.warning("Продавец " + seller_login + " уже в списке избранных покупателя " + buyer_login)
        cursor.close()
        return None


def del_fav_seller(buyer_login, seller_login):
    buyer_login = str(buyer_login)
    seller_login = str(seller_login)
    cursor = connect_db()
    if cursor is None:
        return
    try:
        cursor.execute("DELETE FROM fav_sellers WHERE buyer_login = ? AND seller_login = ?", buyer_login, seller_login)
        cursor.commit()
        log.info("Пользователь " + get_seller(login=seller_login)[1] + " удален из списка покупателя " + get_buyer(login=buyer_login)[1])
    except Exception:
        log.error("Ошибка удаления продавца " + get_seller(login=seller_login)[1] + " из списка покупателя " + get_buyer(login=buyer_login)[1])
    cursor.close()














