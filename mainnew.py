import socket, datetime
import time
from _thread import *

server = "192.168.1.101"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
teraz = datetime.datetime.now()
godzina = int(teraz.strftime("%H"))
minuta = int(teraz.strftime("%M"))
sekunda = int(teraz.strftime(("%S")))
log = open(f"logs\\log{godzina}_{minuta}_{sekunda}.txt", "w", encoding='utf-8')

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(25)

print("Czekanie na połączenie. Server działa")


def to_int(str):
    str = int(str)
    return str


def read_pos(str):
    str = str.split(",")
    str[0] = 'msg_' + str[0]
    return str[0], str[1]


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


currentPlayer = 0

busy_userplace = [0] * 25

pozycje_graczy = [("1", "0")] * 25  # wiadomosc, nadawca
reacts = [("", ""), ("", "")]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pozycje_graczy[player])))
    print(player)
    # conn.send(str.encode("Connected"))
    global currentPlayer
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if "message" in data:
                data = data.split()
                data = data[1]
                data = read_pos(data)

                pozycje_graczy[player] = data
                print(pozycje_graczy)

            if not data:
                print("rozłączono")
                break

            else:
                for i in range(0, 25):
                    if player != i and busy_userplace[i] == 1:
                        reply = pozycje_graczy[i]
                        conn.send(str.encode(make_pos(reply)))
                        time.sleep(0.2)
                # print(type(reply[0]), type(reply[1]))
                teraz = datetime.datetime.now()
                teraz = int(teraz.strftime("%H%M%S"))
                print("otrzymano : ", data)
                log.write(f"otrzymano : {data} + {teraz} \n")
                print("wysyłam : ", reply)
                log.write(f"wysłano : {reply} + {teraz} \n")

        except:
            break

    print("stracono połączenie z :", player)
    busy_userplace[player] = 0
    print(busy_userplace)
    for i in range(0, 25):
        if busy_userplace[i] == 0:
            pozycje_graczy[i] = ("0", "0")
        else:
            break
    conn.close()


while True:

    #

    conn, addr = s.accept()
    for i in range(0, 25):
        if busy_userplace[i] == 0:
            busy_userplace[i] = 1
            currentPlayer = i
            break

    print("połączono z", addr)
    print(busy_userplace)

    start_new_thread(threaded_client, (conn, currentPlayer))

log.close()
