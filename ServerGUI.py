# -*- coding: utf-8 -*-

#from tkinter import ttk
import Tkinter as tk
import database


class ServerGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.db = database.MysqlClass()
        self.var = tk.StringVar()
        self.init_gui()

    def init_gui(self):
        self.master.title("Server")
        self.pack(fill='both', expand=1)

        quit_button = tk.Button(self, text="Quit", command=self.hit)
        quit_button.place(x=0, y=0)

        quit_label = tk.Label(self, textvariable=self.var, bg='white')
        quit_label.place(relx=0.5, rely=0.5, anchor='center')

    def hit(self):
        self.var.set(self.db.get_classwork())


root = tk.Tk()

root.geometry("800x600")
root.resizable(0, 0)
window = ServerGUI(root)
root.mainloop()
