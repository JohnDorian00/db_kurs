import logging
import os
import tkinter

import pygubu
import sign
from db_ctrl import get_all_sellers, update_buyer, get_buyer, get_seller, get_fav_list, del_fav_seller, add_fav_seller

logging.config.fileConfig("conf/logging.conf")
log = logging.getLogger("win_buyer")


def make_fav_list(all_sellers):
    fav_list = get_fav_list(sign.take_user().login)
    fav_sellers = []
    for fav_seller in fav_list:
        for seller in all_sellers:
            if fav_seller == seller[1]:
                fav_sellers.append(seller)
    return fav_sellers


class WinSeller(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('conf/win_ui/buyer.ui')
        self.mainwindow = builder.get_object('frame_buyer', self.master)
        self.set_title("Система управления базой данных. Окно покупателя.")
        builder.connect_callbacks(self)

        self.r_var = tkinter.IntVar()
        rbtn_all = tkinter.Radiobutton(text="Всё", variable=self.r_var, value=0)
        rbtn_city = tkinter.Radiobutton(text="По своему городу", variable=self.r_var, value=1)
        rbtn_all.grid(row=0, column=0, sticky=tkinter.NW, padx=10, pady=115)
        rbtn_city.grid(row=0, column=0, sticky=tkinter.NW, padx=100, pady=115)

        self.user = sign.take_user()
        self.refresh_labels()
        self.refresh_table()

    def update_table_all(self):
        table = self.builder.get_object("tbl_all_price")
        table.delete(*table.get_children())
        sellers = get_all_sellers()
        if sellers is not None:
            for row in sellers:
                if row[2] is None or row[3] is None or row[4] is None:
                    continue
                table.insert("", 'end', values=(row[1], row[2], row[3], row[4]))

    def update_table_fav(self):
        table = self.builder.get_object("tbl_favourites_sellers")
        table.delete(*table.get_children())

        if self.r_var.get() == 1:
            city = get_buyer(self.user.login)[3]
            if city is None:
                return
            else:
                sellers = get_all_sellers(city)
        else:
            sellers = get_all_sellers()
        sellers = make_fav_list(sellers)

        if sellers is not None:
            for row in sellers:
                table.insert("", 'end', values=(row[1], row[2], row[3], row[4]))

    def refresh_data(self):
        fio = self.builder.get_object("inp_fio")
        city = self.builder.get_object("inp_city")
        update_buyer(self.user.login, fio.get(), city.get())
        self.refresh_labels()
        self.refresh_table()

    def refresh_table(self):
        self.update_table_all()
        self.update_table_fav()

    def refresh_labels(self):
        buyer = get_buyer(self.user.login)
        if buyer is None:
            fio = "None"
            city = "None"
        else:
            fio = str(buyer[2])
            city = str(buyer[3])

        lbl_fio = self.builder.get_object("lbl_my_fio")
        lbl_fio.config(text=fio)
        lbl_city = self.builder.get_object("lbl_my_city")
        lbl_city.config(text=city)

    def add_fav_user(self):
        tbl_fav = self.builder.get_object("tbl_all_price")
        elem = tbl_fav.focus()
        elem = tbl_fav.item(elem)["values"]
        if not elem:
            return
        add_fav_seller(self.user.login, elem[0])
        self.refresh_table()

    def del_fav_user(self):
        tbl_fav = self.builder.get_object("tbl_favourites_sellers")
        elem = tbl_fav.focus()
        elem = tbl_fav.item(elem)["values"]
        if not elem:
            return
        del_fav_seller(self.user.login, elem[0])
        self.refresh_table()

    def back(self):
        self.quit()
        sign.startUI()

    def quit(self, event=None):
        self.mainwindow.master.destroy()

    def run(self):
        self.mainwindow.mainloop()

    def take_user(self, user):
        self.user = user


def startUI():
    root = tkinter.Tk()
    icon = os.getcwd() + "/conf/icon.ico"
    root.iconbitmap(icon)
    app = WinSeller(root)
    app.run()
    return
