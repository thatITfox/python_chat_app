import socket
import threading


PORT = 2412
SERVER = input("put your server public ip here: ")
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
USERNAMES = []
OTHERS = []

# send message to the rest of the chat
def SENDMSG(txt,new):
    for PERSON in OTHERS:
        if PERSON != new:
            PERSON.send(txt.encode(FORMAT))


def client_handle(conn, addr):
    # print(f'[NEW CONNECTION] {addr} conneted')
    # get the username of teh client
    msg_length = conn.recv(2048).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    username = msg
    USERNAMES.append(username)
    print("-------------------------------\n"
        f"{username} has join the chat\n"
        "-------------------------------")
    
    SENDMSG("-------------------------------\n"
            f"{username} has join the chat\n"
            "-------------------------------", conn)

    connected = True
    while connected:
        msg_length = conn.recv(2048).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # disconnect from server
            if msg == DISCONNECT_MESSAGE:
                print(f"{USERNAMES[OTHERS.index(conn)]} has left the chat")
                SENDMSG(f"{USERNAMES[OTHERS.index(conn)]} has disconnected",conn)
                USERNAMES.remove(USERNAMES[OTHERS.index(conn)])
                OTHERS.remove(conn)
                connected = False
            
            # check the people are online
            elif msg == "!PEOPLE_ONLINE":
                conn.send(f"people in chat: {USERNAMES}".encode(FORMAT))
            
            # send messages to everyone in the server/chat
            else:
                print(f'{USERNAMES[OTHERS.index(conn)]}: {msg}')
                SENDMSG(f'{USERNAMES[OTHERS.index(conn)]}: {msg}',conn)
    
    conn.close()


# start the server
def start():
    server.listen()
    print(f'[LISTENING] Sever is listening on {SERVER}')
    while True:
        # accept any request comming trough
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handle, args=(conn, addr))
        thread.start()
        OTHERS.append(conn)
        print(f'\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
        print(USERNAMES)


print('[STARTING] server is starting....')
start()
