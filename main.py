import socket
from threading import Thread
from time import sleep
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image

import utils
from utils import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
FORMAT = "utf-8"


class Frames(object):

    def __init__(self):
        self.d_text = None
        self.msg = ''
        self.running = False
        self.font = 'Arial'
        self.font_logo = 'Comic Sans MS'

        self.debug = 0
        self.theme = 0

        self.background_color = '#ffffff'
        self.background_color_light = '#f4f4f4'
        self.font_color = '#000000'
        self.d_background_color = '#1c1c1c'
        self.d_background_color_light = '#313131'
        self.d_font_color = '#ebebeb'

        self.przekl = ['jeba', 'kurw', 'huj', 'cwel', 'pedał', 'pedal', 'dziwk', 'fuck', 'pierdol', 'zajeb', 'zjeb',
                       'wypierdalaj', 'spierdalaj', 'cunt', 'pussy', 'pizd', 'cip', 'kurv', 'nigg', 'porn']

    def exit_button(self, root):
        root.destroy()
        self.running = False
        client.close()
        exit(0)

    def change_theme(self, root):
        if self.theme == 0:
            # self.background_color = '#1c1c1c'
            # self.background_color_light = '#313131'
            # self.font_color = '#ebebeb'
            self.m_frame.config(bg=self.d_background_color)
            self.m_l_logo.config(bg=self.d_background_color, fg=self.d_font_color)
            self.m_b_settings.config(bg=self.d_background_color_light, fg=self.d_font_color, text='Jasny')
            self.m_b_exit.config(bg=self.d_background_color_light, fg=self.d_font_color)
            self.m_t.config(bg=self.d_background_color_light, fg=self.d_font_color)
            self.m_ent.config(bg=self.d_background_color_light, fg=self.d_font_color)
            self.m_b_send.config(bg=self.d_background_color_light, fg=self.d_font_color)
            self.m_l_info.config(bg=self.d_background_color, fg=self.d_font_color)

            self.theme = 1
            root.update()
        elif self.theme == 1:
            self.m_frame.config(bg=self.background_color)
            self.m_l_logo.config(bg=self.background_color, fg=self.font_color)
            self.m_b_settings.config(bg=self.background_color_light, fg=self.font_color, text='Ciemny')
            self.m_b_exit.config(bg=self.background_color_light, fg=self.font_color)
            self.m_t.config(bg=self.background_color_light, fg=self.font_color)
            self.m_ent.config(bg=self.background_color_light, fg=self.font_color)
            self.m_b_send.config(bg=self.background_color_light, fg=self.font_color)
            self.m_l_info.config(bg=self.background_color, fg=self.font_color)
            self.theme = 0
            root.update()

    def login_compl(self, root, entry_ip, entry):
        # 192.168.1.101
        if entry_ip.get() != "" and entry.get() != "":
            try:
                client.connect((entry_ip.get(), 5555))
                client.send(self.name.get().encode(FORMAT))
                self.frame.destroy()
                self.main_frame(root)
            except:
                messagebox.showerror('Niepoprawne IP', 'Niepoprawne IP.\nSpróbuj ponownie.')

    def login_compl_ev(self, event, root, entry_ip, entry):
        if entry_ip.get() != "" and entry.get() != "":
            try:
                client.connect((entry_ip.get(), 5555))
                client.send(self.name.get().encode(FORMAT))
                self.frame.destroy()
                self.main_frame(root)
            except:
                messagebox.showerror('Niepoprawne IP', 'Niepoprawne IP.\nSpróbuj ponownie.')

    def set_msg(self, result):
        self.msg = result

    def close_debug(self, droot):
        droot.destroy()
        self.debug = 0

    def debug_window(self, event):
        droot = Tk.Toplevel(root)
        droot.title = 'Debug'
        droot.resizable(False, False)

        self.debug = 1

        dframe = Tk.Frame(droot, bg=self.d_background_color)
        dframe.pack(side="top", expand=True, fill=Tk.BOTH)

        l_debug = Tk.Label(dframe, text='Debug', bg=self.d_background_color, fg=self.d_font_color)
        l_debug.grid(column=0, row=0, padx=5, pady=5, sticky='w')

        b_exit = Tk.Button(dframe, text='Wyjdź', command=lambda: self.close_debug(droot),
                           bg=self.d_background_color_light, fg=self.d_font_color)
        b_exit.grid(column=1, row=0, padx=5, pady=5, sticky='e')

        self.d_text = Tk.Text(dframe, bg=self.d_background_color_light, fg=self.d_font_color)
        self.d_text.config(state=Tk.DISABLED)
        self.d_text.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.m_frame.columnconfigure(1, weight=1)
        self.m_frame.rowconfigure(1, weight=1)

        droot.update()

        droot.mainloop()

    def update_debug(self, msg):
        self.d_text.config(state=Tk.NORMAL)
        self.d_text.insert(Tk.END, '[D] ' + msg)
        self.d_text.yview_moveto(1)
        self.d_text.config(state=Tk.DISABLED)

    def receive(self, root, t):
        last_message = ''
        list_usernames = [""] * 25
        list_lmessages = [""] * 25
        while 1:
            if not self.running:
                break
            client.send("ping".encode(FORMAT))
            data_odb = client.recv(4096).decode()
            # data = utils.decrypt(data_odb)
            data = data_odb
            if data:
                m = data.split(',')
                if self.debug:
                    self.update_debug(str(m) + '\n')
                wiadomosc = m[0]
                user = m[1]
                user = user.replace("ping", "")
                if wiadomosc.startswith("msg"):
                    if user not in list_usernames:
                        for i in range(0, 25):
                            if list_usernames[i] == "":
                                list_usernames[i] = user
                                break
                    wiadomosc = wiadomosc.replace("msg_", "")

                    if self.debug:
                        self.update_debug(wiadomosc + '\n')
                    if "§" in wiadomosc:
                        wiadomosc = wiadomosc.replace("§", " ")
                    if self.debug:
                        self.update_debug(str(list_usernames) + '\n')
                        self.update_debug(str(list_lmessages) + '\n')
                    for i in range(0, 25):
                        if list_usernames[i] == user:
                            if self.debug:
                                self.update_debug(str(list_lmessages) + '\n')
                            if list_lmessages[i] != wiadomosc:
                                x = user + ' -> ' + wiadomosc + '\n'
                                t.config(state=Tk.NORMAL)
                                t.insert(Tk.END, x)
                                t.config(state=Tk.DISABLED)
                                list_lmessages[i] = wiadomosc
                                break
            root.update()
            sleep(0.1)

    def con(self, root, t):
        Thread(target=lambda: self.receive(root, t)).start()
        # data = ['b', 'a']
        # while 1:
        #     last_message = 'b'
        #     if " " in self.msg:
        #         self.msg = self.msg.replace(" ", "§•")
        #     if self.msg != "":
        #         msgclient = "message " + f'{self.msg},{self.name}'
        #         data = client.send(msgclient.encode(FORMAT))
        #     wiadomosc = data[0]
        #     user = data[1]
        #
        #     if "§•" in wiadomosc:
        #         wiadomosc = wiadomosc.replace("§•", " ")
        #
        #     if wiadomosc != "" and wiadomosc != last_message:
        #         print(user, "→", wiadomosc)
        #         x = (user, wiadomosc)
        #         t.insert('', Tk.END, values=x)
        #     last_message = wiadomosc
        #     root.update()
        #     if 'normal' != root.state():
        #         break

    def login_frame(self, root):
        root.title('SuperŻerom')
        root.geometry("400x700")
        root.resizable(0, 0)

        self.frame = Tk.Frame(root, width=800, height=600, background=self.background_color)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        l_logo = Tk.Label(self.frame, text="SuperŻerom", font=(self.font_logo, 30), background=self.background_color,
                          fg=self.font_color)
        l_logo.grid(column=0, row=0, columnspan=3, sticky='we', pady=5, padx=5)

        self.name = Tk.StringVar()

        img = Image.open('images/spider.png')
        l_img = Tk.Label(self.frame)
        l_img.img = ImageTk.PhotoImage(img)
        l_img['image'] = l_img.img
        l_img.grid(column=1, row=1, padx=5, pady=5)

        l_ip = Tk.Label(self.frame, text='IP:', bg=self.background_color)
        l_ip.grid(column=1, row=2, sticky='we', padx=5)
        ent_ip = Tk.Entry(self.frame, font=(self.font, 10), bg=self.background_color_light,
                          fg=self.font_color, justify=Tk.CENTER)
        # TODO wykasuj to
        ent_ip.insert(0, '192.168.1.101')
        ent_ip.grid(column=1, row=3, sticky='we', pady=5, padx=5)

        l_name = Tk.Label(self.frame, text='Nazwa:', bg=self.background_color)
        l_name.grid(column=1, row=4, sticky='we', padx=5)
        ent = Tk.Entry(self.frame, textvariable=self.name, font=(self.font, 10), bg=self.background_color_light,
                       fg=self.font_color, justify=Tk.CENTER)
        ent.grid(column=1, row=5, sticky='we', pady=5, padx=5)

        button = Tk.Button(self.frame, text='Połącz', font=(self.font, 12),
                           command=lambda: self.login_compl(root, ent_ip, ent),
                           bg=self.background_color_light, fg=self.font_color)
        button.grid(column=1, row=6, pady=10, padx=5)

        ent_ip.focus_set()

        root.bind('<Return>', lambda event: self.login_compl_ev(event, root, ent_ip, ent))

    def main_frame(self, root):
        root.title('SuperŻerom')
        root.geometry("800x600")
        root.resizable(0, 0)

        self.running = True
        client.send("ping".encode(FORMAT))

        # STYLES
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Comic Sans MS', 15))
        style.configure("Treeview", font=('Comic Sans MS', 12))

        root.bind('<Return>',
                  lambda event: utils.send_message_enter(event, self.m_t, self.m_ent, client, FORMAT, self.name.get(),
                                                         self.przekl))
        if not self.debug:
            root.bind('<F10>', lambda event: self.debug_window(event))

        self.m_frame = Tk.Frame(root, width=800, height=600, bg=self.background_color)
        self.m_frame.pack(side="top", fill="both", expand=True)

        self.m_l_logo = Tk.Label(self.m_frame, text='SuperŻerom', font=(self.font_logo, 25), bg=self.background_color,
                                 fg=self.font_color)
        self.m_l_logo.grid(column=0, row=0, sticky='w', pady=5, padx=5)

        self.m_b_settings = Tk.Button(self.m_frame, text='Ciemny', font=(self.font, 12), bg=self.background_color_light,
                                      fg=self.font_color, command=lambda: self.change_theme(root))
        self.m_b_settings.grid(column=1, row=0, sticky='e', padx=5)

        self.m_b_exit = Tk.Button(self.m_frame, text='Rozłącz', command=lambda: self.exit_button(root),
                                  font=(self.font, 12),
                                  bg=self.background_color_light,
                                  fg=self.font_color)
        self.m_b_exit.grid(column=2, row=0, sticky='ew', padx=5)



        # threeview

        self.m_t = Tk.Text(self.m_frame, font=(self.font, 15), bg=self.background_color_light, fg=self.font_color)
        self.m_t.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5, padx=5)
        self.m_t.config(state=Tk.DISABLED)

        # messages = []
        # for i in range(1,100):
        #     messages.append((f'nick {i}', f'message {i}'))
        #
        # for message in messages:
        #     t.insert('', Tk.END, values=message)

        self.m_frame.columnconfigure(1, weight=1)
        self.m_frame.rowconfigure(1, weight=1)

        self.m_ent = Tk.Entry(self.m_frame, bg=self.background_color_light, fg=self.font_color)
        self.m_ent.grid(column=0, row=3, columnspan=2, sticky='ew', pady=5, padx=5)

        # utils.send_message(t, ent, client, FORMAT, self.name.get())
        self.m_b_send = Tk.Button(self.m_frame, text='>', font=(self.font, 12),
                                  command=lambda: utils.send_message(self.m_t, self.m_ent, client, FORMAT,
                                                                     self.name.get(), self.przekl),
                                  bg=self.background_color_light, fg=self.font_color)
        self.m_b_send.grid(column=2, row=3, sticky='ew', pady=5, padx=5)

        self.m_l_info = Tk.Label(self.m_frame, text=f'Zalogowany jako: {self.name.get()}', font=(self.font, 8),
                                 bg=self.background_color, fg=self.font_color)
        self.m_l_info.grid(column=0, row=4, columnspan=3)

        root.update()

        self.m_ent.focus_set()

        self.con(root, self.m_t)


root = Tk.Tk()
app = Frames()
app.login_frame(root)
root.mainloop()