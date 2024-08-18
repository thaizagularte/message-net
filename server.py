
from socket import *
import threading
HOST = '127.0.0.1'
PORT=2000
clients = []

def msgs(c):
    while True:
        try:
            msg = c.recv(1024).decode()
            if not msg:
                continue
            print(msg)
            if "exit" in msg:
                c.close()
                break
        except:
            clients.remove(c)
            break

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=msgs,args=[conn])
        client_thread.start()

exit()


