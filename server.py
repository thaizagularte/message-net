
from socket import *
import threading
HOST = '127.0.0.1'
PORT = 20022
clients = []

def msgs(c):
    while True:
        try:
            msg = c.recv(1024)
            if not msg:
                continue
            print(msg.decode())
        except Exception as e:
            print(f'Erro {e}')
            clients.remove(c)
            break

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        print(conn, addr)
        client_thread = threading.Thread(target=msgs,args=[conn])
        client_thread.start()

exit(0)


