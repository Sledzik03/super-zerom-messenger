import tkinter as Tk


def send_message(t, ent, client, FORMAT, name, przekl):
    msg = ent.get()
    legit = 1
    for x in przekl:
        if x in msg:
            legit = 0
            t.config(state=Tk.NORMAL)
            t.insert(Tk.END, 'Proszę nie przeklinać cwaniaczku\n')
            t.config(state=Tk.DISABLED)
            t.yview_moveto(1)
            ent.delete(0, Tk.END)
    if legit:
        msgclient = "message " + msg.replace(" ", "§") + "," + name
        if msg:
            # client.send(encrypt(msgclient).encode())
            client.send(msgclient.encode())
            x = name + ' -> ' + msg + '\n'
            t.config(state=Tk.NORMAL)
            t.insert(Tk.END, x)
            t.config(state=Tk.DISABLED)
            t.yview_moveto(1)
            ent.delete(0, Tk.END)


def send_message_enter(event, t, ent, client, FORMAT, name, przekl):
    msg = ent.get()
    legit = 1
    for x in przekl:
        if x in msg:
            legit = 0
            t.config(state=Tk.NORMAL)
            t.insert(Tk.END, 'Proszę nie przeklinać cwaniaczku\n')
            t.config(state=Tk.DISABLED)
            t.yview_moveto(1)
            ent.delete(0, Tk.END)
    if legit:
        msgclient = "message " + msg.replace(" ", "§") + "," + name
        if msg:
            # client.send(encrypt(msgclient).encode())
            client.send(msgclient.encode())
            x = name + ' -> ' + msg + '\n'
            t.config(state=Tk.NORMAL)
            t.insert(Tk.END, x)
            t.config(state=Tk.DISABLED)
            t.yview_moveto(1)
            ent.delete(0, Tk.END)


def encrypt(plaintext):
    cipher_text = ""
    przes = 19

    for i in range(len(plaintext)):
        char = plaintext[i]
        if 65 <= ord(char) <= 90:
            cipher_text += chr((ord(char) + przes - 65) % 26 + 65)
        elif 97 <= ord(char) <= 122:
            cipher_text += chr((ord(char) + przes - 97) % 26 + 97)
    return cipher_text


def decrypt(plaintext):
    cipher_text = ""
    przes = 19

    for i in range(len(plaintext)):
        char = plaintext[i]
        if 65 <= ord(char) <= 90:
            cipher_text += chr((ord(char) - przes - 65) % 26 + 65)
        elif 97 <= ord(char) <= 122:
            cipher_text += chr((ord(char) - przes - 97) % 26 + 97)
    return cipher_text
