import os
import numpy as np
import sign
from tkinter import *
from PIL import Image, ImageTk


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = np.load("conf/ee.npy")
        load = Image.fromarray(load)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


def on_closing():
    root.destroy()
    sign.startUI()


def startUI():
    global root
    root = Tk()
    icon = os.getcwd() + "/conf/icon.ico"
    root.iconbitmap(icon)
    Window(root)
    root.wm_title("easter+egg")
    root.geometry("411x239")
    root.minsize("411", "239")
    root.maxsize("411", "239")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    return