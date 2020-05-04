import os
import tkinter
import dlg_add_user
import sign
import pygubu
from db_ctrl import get_all_users, del_user


class WinManager(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('conf/win_ui/manager.ui')
        self.mainwindow = builder.get_object('frame_manager', self.master)
        self.set_title("Система управления базой данных. Окно менеджера.")
        builder.connect_callbacks(self)

        self.user = sign.take_user()
        self.refresh_labels()
        self.update_table()

    def update_table(self):
        table = self.builder.get_object("tbl_users")
        table.delete(*table.get_children())
        users = get_all_users()
        if users is not None:
            for row in users:
                table.insert("", 'end', values=(row[0], row[1], row[3]))

    @staticmethod
    def add_user():
        dlg_add_user.startUI()

    def del_user(self):
        table = self.builder.get_object("tbl_users")
        elem = table.focus()
        elem = table.item(elem)["values"]
        if not elem or str(elem[1]) == str(self.user.login):
            return
        else:
            del_user(elem[1])
            self.update_table()

    def refresh(self):
        self.update_table()

    def refresh_labels(self):
        lbl_fio = self.builder.get_object("lbl_login")
        lbl_fio.config(text=self.user.login)

    def back(self):
        self.quit()
        sign.startUI()

    def quit(self, event=None):
        self.mainwindow.master.destroy()

    def run(self):
        self.mainwindow.mainloop()


def startUI():
    root = tkinter.Tk()
    icon = os.getcwd() + "/conf/icon.ico"
    root.iconbitmap(icon)
    root.geometry("480x340")
    root.minsize("480","340")
    app = WinManager(root)
    app.run()
    return
