
from socket import *
import threading
HOST = '192.168.8.13'
PORT = 20022
clients = []

def msgs(c):
    while True:
        try:
            msg = c.recv(1024)
            if not msg:
                continue
            r_msg(c, msg)
            print(msg.decode())
        except Exception as e:
            print(f'Erro {e}')
            clients.remove(c)
            break

def r_msg(c, data):
    for client in clients:
        if client != c:
            client.send(data)

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print(conn, addr)
        clients.append(conn)
        client_thread = threading.Thread(target=msgs,args=[conn])
        client_thread.start()

exit(0)


