import socket
import threading

print("                 __  .__                                  .__  .__        \n"
"______ ___.__._/  |_|  |__   ____   ____     ____   ____ |  | |__| ____   ____  \n"
"\____ <   |  |\   __\  |  \ /  _ \ /    \   /  _ \ /    \|  | |  |/    \_/ __ \ \n"
"|  |_> >___  | |  | |   Y  (  <_> )   |  \ (  <_> )   |  \  |_|  |   |  \  ___/ \n"
"|   __// ____| |__| |___|  /\____/|___|  /  \____/|___|  /____/__|___|  /\___  >\n"
"|__|   \/                \/            \/              \/             \/     \/ \n"
"       .__            __                                                        \n"
"  ____ |  |__ _____ _/  |_  _____  ______ ______                                \n"
"_/ ___\|  |  \\\\__  \\\\   __\ \__  \ \____ \\\\____ \                         \n"
"\  \___|   Y  \/ __ \|  |    / __ \|  |_> >  |_> >                              \n"
" \___  >___|  (____  /__|   (____  /   __/|   __/                               \n"
"     \/     \/     \/            \/|__|   |__|                                  \n"
)
print("V1.0.0")
print("created by thatITfox")
print("based from https://github.com/nimiology/local_massenger_socket")
print("more version comming to the future")

WORKING = True
SERVER = input('What is the server IP?')
PORT = int(input('What is the server PORT?'))
USERNAME = input("enter your username here: ")
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
print('[CONNECTION] connected successfully')

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(2048 - len(send_length))
    client.send(send_length)
    client.send(message)

def RECIVER():
    while WORKING:
        DATA = client.recv(2048).decode(FORMAT)
        print(DATA)

print(f"if you want to exit type : {DISCONNECT_MESSAGE}")
print(f"to see the people wo is online type: !PEOPLE_ONLINE")
THREAD = threading.Thread(target=RECIVER)
THREAD.start()

# send the username to the server
send(USERNAME)
while WORKING:
    MSG = input()
    send(MSG)
    if MSG == DISCONNECT_MESSAGE:
        WORKING = False
        exit()
