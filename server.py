import socket
import threading


PORT = 2412
SERVER = input("put your server public ip here: ")
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
USERNAMES = []
OTHERS = []
PASSWORD = input("put in your server password here: ")

# send message to the rest of the chat
def SENDMSG(txt,new):
    for PERSON in OTHERS:
        if PERSON != new:
            PERSON.send(txt.encode(FORMAT))

def client_handle(conn, addr):
    # get the username of the client
    msg_length = conn.recv(2048).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    username = msg

    psw_length = conn.recv(2048).decode(FORMAT)
    if psw_length:
        psw_length = int(psw_length)
        password = conn.recv(psw_length).decode(FORMAT)

    if password == PASSWORD:
        USERNAMES.append(username)
        print(f'\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
        print(USERNAMES)
        conn.send(f"welcome {username} to the server ^^".encode(FORMAT))
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
                if msg == "/quit":
                    print(f"{username} has left the chat")
                    SENDMSG(f"{username} has disconnected",conn)
                    USERNAMES.remove(username)
                    OTHERS.remove(conn)
                    connected = False
                
                # check the people are online
                elif msg == "/whoisonline":
                    conn.send(f"people in chat: {USERNAMES}".encode(FORMAT))
                
                # send messages to everyone in the server/chat
                else:
                    print(f'{username}: {msg}')
                    SENDMSG(f'{username}: {msg}',conn)
    else:
        conn.send("sorry you got the wrong password :(".encode(FORMAT))
        OTHERS.remove(conn)
    
    conn.close()


# start the server
def start():
    server.listen()
    print(f'[LISTENING] Sever is listening on {SERVER}')
    while True:
        # accept any request coming trough
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handle, args=(conn, addr))
        thread.start()
        OTHERS.append(conn)


print('[STARTING] server is starting....')
start()
