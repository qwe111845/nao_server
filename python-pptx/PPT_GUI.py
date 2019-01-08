# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox as tm
import database
import os
import tkFileDialog
from pptx import Presentation
import win32com
import win32com.client
from PIL import Image, ImageTk
import io
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ServerGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.db = database.MysqlClass()
        self.var = tk.StringVar()
        self.ppt_file = ''
        self.save_dir = ''
        self.jpg_dir = ''
        self.ppt_number = 0
        self.ppt_len = 0
        self.ppt_text = []
        self.init_gui()

    def init_gui(self):
        self.master.title("PPT播放工具")
        self.pack(fill='both', expand=1)

        self.ip_text = tk.Text(self)
        self.ip_text.place(relx=0.85, relheight=0.05, relwidth=0.15)

        link_button = tk.Button(self, text='Link robot', command=self.link_nao)
        link_button.place(relx=0.85, rely=0.05, relheight=0.03, relwidth=0.15)

        self.link_label = tk.Label(self, textvariable='尚未連線', bg='LightCyan')
        self.link_label.place(relx=0.85, rely=0.08, relheight=0.05, relwidth=0.15)

        ppt_selection_button = tk.Button(self, text="選擇文件", command=self.set_data)
        ppt_selection_button.place(relx=0.85, rely=0.13, relheight=0.05, relwidth=0.15)

        start_button = tk.Button(self, text="Start", command=self.ppt_set)
        start_button.place(relx=0.85, rely=0.18, relheight=0.04, relwidth=0.15)

        previous_button = tk.Button(self, text="Previous slide", command=self.previous_ppt)
        previous_button.place(relx=0.85, rely=0.22, relheight=0.04, relwidth=0.075)

        next_button = tk.Button(self, text="Next slide", command=self.next_ppt)
        next_button.place(relx=0.925, rely=0.22, relheight=0.04, relwidth=0.075)

        speak_button = tk.Button(self, text="Speak", command=self.ppt_set)
        speak_button.place(relx=0.85, rely=0.18, relheight=0.04, relwidth=0.15)

        quit_button = tk.Button(self, text="Quit PPT Mode", command=self.ppt_set)
        quit_button.place(relx=0.85, rely=0.18, relheight=0.04, relwidth=0.15)

        self.ppt_label = tk.Label(self, textvariable=self.var, bg='white')
        self.ppt_label.place(relheight=1, relwidth=0.85)

        self.text_label = tk.Label(self, textvariable=self.var, bg='gray',
                              wraplength=150, anchor='nw', justify='left')
        self.text_label.place(relx=0.85, rely=0.4, relheight=0.6, relwidth=0.15)

    def text_set(self, text_list):
        set_text = ''
        for i, text in enumerate(text_list):
            set_text += str(i+1) + '.\n' + str(text) + '\n'

        self.var.set(set_text)

        if int(self.text_label.winfo_width()/13) >= 14:
            fontsize = 14
        else:
            fontsize = 10
        self.text_label.config(font=("Helvetica", fontsize, 'bold'), wraplength=self.text_label.winfo_width()-5)

    def set_data(self):
        default_dir = r"C:\Users\lin\Desktop"
        self.ppt_file = tkFileDialog.askopenfilename(title="選擇文件",
                                                     initialdir=(os.path.expanduser(default_dir)))

        self.save_dir = tkFileDialog.askdirectory(title="儲存的資料夾")

        if len(self.ppt_file) <= 0 or len(self.save_dir) <= 0:
            tm.showinfo(title='wrong', message='請選擇文件及儲存的資料夾')
            pass
        else:
            if len(self.ppt_file) > 0:
                fstart = self.ppt_file.rindex('/')
                self.fname = self.ppt_file[fstart + 1:-5]

            self.ppt_file = self.ppt_file.replace('/', r'\\')
            self.save_dir = self.save_dir.replace('/', r'\\')

            self.ppt2png(self.fname, self.ppt_file, self.save_dir)

    def link_nao(self):
        ip = self.ip_text.get("1.0", "end-1c")
        if len(ip) <= 0:
            tm.showinfo(title='wrong', message='請輸入ip位址')
        else:


    def img_set(self):
        w_box = self.ppt_label.winfo_width()
        h_box = self.ppt_label.winfo_height()
        img_location = self.save_dir + r"\\" + self.fname + r"\\投影片" + str(self.ppt_number + 1) + r".jpg"

        pil_image = Image.open(img_location)
        pil_image_resized = self.resize(w_box, h_box, pil_image)

        tk_image = ImageTk.PhotoImage(pil_image_resized)
        self.ppt_label.config(image=tk_image)
        self.ppt_label.image = tk_image

        self.text_set(self.ppt_text[self.ppt_number])

    def ppt_set(self):
        if len(self.save_dir) == 0 or len(self.fname) == 0:
            tm.showinfo(title='wrong', message='請先選擇儲存的資料夾')
            pass
        else:
            self.jpg_dir = self.save_dir + r"\\" + self.fname + r"\\"
            self.ppt_number = 0
            self.img_set()

    def previous_ppt(self):
        if len(self.save_dir) == 0 or len(self.fname) == 0:
            tm.showinfo(title='wrong', message='沒有投影片')
            pass
        elif self.ppt_number == 0:
            tm.showinfo(title='wrong', message='沒有上一頁投影片')
            pass
        else:
            self.ppt_number -= 1
            self.img_set()

    def next_ppt(self):
        if len(self.save_dir) == 0 or len(self.fname) == 0:
            tm.showinfo(title='wrong', message='沒有投影片')
            pass
        elif self.ppt_number == self.ppt_len-1:
            tm.showinfo(title='wrong', message='已經是最後一頁投影片')
            pass
        else:
            self.ppt_number += 1
            self.img_set()

    def ppt2png(self, ppt_file_name, ppt_path, save_path):

        powerpoint = win32com.client.Dispatch('PowerPoint.Application')
        powerpoint.Visible = True
        ppt = powerpoint.Presentations.Open(ppt_path)
        ppt.SaveAs(save_path + r'\\' + ppt_file_name.rsplit('.')[0], 17)
        ppt.Close()
        powerpoint.Quit()

        prs = Presentation(self.ppt_file)
        self.ppt_len = len(prs.slides)

        for slide in prs.slides:
            for shape in slide.shapes:
                text_runs = []
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    text = ''
                    for run in paragraph.runs:
                        text += run.text
                    text_runs.append(text)
            self.ppt_text.append(text_runs)

    def resize(self, w_box, h_box, pil_image):
        w, h = pil_image.size
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)


root = tk.Tk()
root.geometry("1280x960")
root.minsize(1024,768)
window = ServerGUI(root)
root.mainloop()
