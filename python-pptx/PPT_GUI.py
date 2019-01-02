# -*- coding: utf-8 -*-

#from tkinter import ttk
import Tkinter as tk
import database
import os
import tkFileDialog
from pptx import Presentation
import win32com
import win32com.client

class ServerGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.db = database.MysqlClass()
        self.var = tk.StringVar()
        self.ppt_file = ''
        self.save_dir = ''
        self.ppt_number = 0
        self.init_gui()

    def init_gui(self):
        self.master.title("Server")
        self.pack(fill='both', expand=1)

        self.ip_text = tk.Text(self)
        self.ip_text.place(relx=0.85, relheight=0.05, relwidth=0.15)

        link_button = tk.Button(self, text='link robot',command=self.link_nao)
        link_button.place(relx=0.85, rely=0.05, relwidth=0.15)

        start_button = tk.Button(self, text="選擇文件", command=self.get_data)
        start_button.place(relx=0.85, rely=0.15, relwidth=0.15)

        talk_button = tk.Button(self, text="start", command=self.hit)
        talk_button.place(relx=0.85, rely=0.19, relwidth=0.15)

        ppt_label = tk.Label(self, textvariable=self.var, bg='white')
        ppt_label.place(relheight=1, relwidth=0.85)

    def hit(self):
        self.var.set(self.db.get_classwork())

    def get_data(self):
        default_dir = r"C:\Users\lin\Desktop"
        self.ppt_file = tkFileDialog.askopenfilename(title="選擇文件",
                                             initialdir=(os.path.expanduser(default_dir)))
        self.save_dir = tkFileDialog.askdirectory()

        fstart = self.ppt_file.rindex('/')
        self.fname = self.ppt_file[fstart+1:]



    def link_nao(self):
        print self.ip_text.get("1.0", "end-1c")

    def image_set(self):
        set = 0

    def ppt2png(pptFileName, ppt_path, save_path):

        powerpoint = win32com.client.Dispatch('PowerPoint.Application')
        powerpoint.Visible = True
        ppt = powerpoint.Presentations.Open(ppt_path)
        ppt.SaveAs(save_path + pptFileName.rsplit('.')[0], 17)
        ppt.Close()
        powerpoint.Quit()

        prs = Presentation(self.ppt_file)
        for slide in prs.slides:
            for shape in slide.shapes:
                text = ''
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text += run.text
                text_runs.append(text)


root = tk.Tk()

root.geometry("1280x960")
window = ServerGUI(root)
root.mainloop()
