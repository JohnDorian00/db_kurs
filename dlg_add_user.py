import logging
import os
import tkinter
from tkinter import messagebox
import sign
from user import User

from db_ctrl import add_user, get_user

import pygubu

logging.config.fileConfig("conf/logging.conf")
log = logging.getLogger("win_dlg_add_user")


class WinDlgAddUser(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('conf/win_ui/dlg_add_user.ui')
        self.mainwindow = builder.get_object('dlg_add_user', self.master)
        self.set_title("Добавить пользователя")
        builder.connect_callbacks(self)

    def add_user(self):
        if sign.take_user() is None:
            log.warning("Попытка добавить пользователя при неактивном аккаунте")
            self.quit()
            return
        login = self.builder.get_object("inp_login")
        pass1 = self.builder.get_object("inp_pass")
        pass2 = self.builder.get_object("inp_pass2")
        user_type = self.builder.get_object("inp_type")

        u = get_user(login=login.get())

        if login.get() == "":
            print("None")

        if u.id is None:
            if login.get() != "":
                if pass1.get() == pass2.get():
                    if user_type.get() != "":
                        add_user(User("", login.get(), pass1.get(), user_type.get()))
                        messagebox.showinfo("Успех!",
                                            "Добавлен пользователь " + login.get() + " с правами " + user_type.get())
                        self.quit()
                    else:
                        messagebox.showerror("Неудача", "Укажите тип пользователя!")
                else:
                    messagebox.showerror("Неудача", "Пароли не совпадают!")
            else:
                messagebox.showerror("Неудача", "Не введен логин!")
        else:
            messagebox.showerror("Неудача!", "Пользователь с логином " + login.get() + " уже существует ")

    def quit(self, event=None):
        self.mainwindow.master.destroy()

    def run(self):
        self.mainwindow.mainloop()


def startUI():
    root = tkinter.Tk()
    icon = os.getcwd() + "/conf/icon.ico"
    root.iconbitmap(icon)
    app = WinDlgAddUser(root)
    app.run()
    return
