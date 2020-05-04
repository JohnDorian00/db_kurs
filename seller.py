import os
import tkinter
import pygubu
import sign
from db_ctrl import get_all_sellers, update_seller, get_seller


class WinSeller(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('conf/win_ui/seller.ui')
        self.mainwindow = builder.get_object('frame_seller', self.master)
        self.set_title("Система управления базой данных. Окно продавца.")
        builder.connect_callbacks(self)

        self.user = sign.take_user()
        self.refresh_labels()
        self.update_table()

    def update_table(self):
        table = self.builder.get_object("tbl_city_price")
        table.delete(*table.get_children())
        sellers = get_all_sellers()
        if sellers is not None:
            for row in sellers:
                if row[2] is None or row[3] is None or row[4] is None:
                    continue
                table.insert("", 'end', values=(row[3], row[4]))

    def refresh_data(self):
        fio = self.builder.get_object("inp_fio")
        city = self.builder.get_object("inp_city")
        avg_price = self.builder.get_object("inp_avg_price")
        update_seller(self.user.login, fio.get(), city.get(), avg_price.get())
        self.refresh_labels()
        self.update_table()

    def refresh_table(self):
        self.update_table()

    def refresh_labels(self):
        seller = get_seller(self.user.login)
        if seller is None:
            fio = "None"
            city = "None"
            avg_price = "None $"
        else:
            fio = str(seller[2])
            city = str(seller[3])
            avg_price = str(seller[4]) + " $"

        lbl_fio = self.builder.get_object("lbl_my_fio")
        lbl_fio.config(text=fio)
        lbl_city = self.builder.get_object("lbl_my_city")
        lbl_city.config(text=city)
        lbl_avg_price = self.builder.get_object("lbl_my_price")
        lbl_avg_price.config(text=avg_price)

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
    app = WinSeller(root)
    app.run()
    return
