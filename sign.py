import hashlib
import os
import tkinter
import buyer
import seller
import manager
import pygubu
import logging.config
# import ee
# from main import for_pygubu, hex
from db_ctrl import get_user
from tkinter import messagebox

start_win = {
    "MANAGER": manager.startUI,
    "BUYER": buyer.startUI,
    "SELLER": seller.startUI,
}

logging.config.fileConfig("conf/logging.conf")
log = logging.getLogger("win_sign")


class WinSign(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('conf/win_ui/sign.ui')
        self.mainwindow = builder.get_object('frame_sign', self.master)
        self.set_title("Система управления базой данных. Окно аутентификации пользователя.")
        builder.connect_callbacks(self)
        global u
        u = None

    def open_win_main(self):
        login = self.builder.get_object("inp_login")
        password = self.builder.get_object("inp_pass")
        # if check_stamp(for_pygubu, login.get()) and check_stamp(hex, password.get()):
        #     self.quit()
        #     ee.startUI()
        #     return

        global u
        u = get_user(login=login.get())
        if u is not None and u.id is not None:
            if u.auth(password.get()):
                self.quit()
                start_win[u.user_type]()
            else:
                log.info("Неверно введен пароль, логин - " + login.get() + ", пароль - " + password.get())
                messagebox.showerror("Неудача", "Неверный пароль!")
        else:
            messagebox.showinfo("Неудача", "Пользователя с таким именем не существует")

    def quit(self, event=None):
        self.mainwindow.master.destroy()

    def run(self):
        self.mainwindow.mainloop()


def take_user():
    return u


# def check_stamp(data, verified_data):
#     data, salt = data.split(':')
#     return data == hashlib.sha512(salt.encode() + verified_data.encode()).hexdigest()


def startUI():
    root = tkinter.Tk()
    icon = os.getcwd() + "/conf/icon.ico"
    root.iconbitmap(icon)
    app = WinSign(root)
    app.run()
    return



