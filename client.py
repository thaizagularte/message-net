import threading
from dataclasses import dataclass
from socket import *
from time import sleep

HOST = '192.168.8.13'
PORT = 20023




def send_msg(c, u):
    while True:
        try:
            msg = input("Input: ")
            c.send(f'<{u}> {msg}'.encode('utf-8'))
        except Exception as e:
            print(e)
            return

def recv_msg(c):
    while True:
        try:
            msg = c.recv(1024)
            if not msg:
                break

            print(f'{msg.decode()}\n')
        except Exception as e:
            print(e)
    c.close()



print("### CHAT ###")

user = input("Insira o seu nome para inicar a conexão: ")
client = socket(AF_INET, SOCK_STREAM)

print("Iniciando Conexão")

try:
    client.connect((HOST, PORT))
    print(f'Conectado como {user}!')
except Exception as e:
    print(e)
    print("Erro ao conectar\nSaindo", end="")
    exit(0)
send_thread = threading.Thread(target=send_msg, args=[client, user])
recv_thread = threading.Thread(target=recv_msg, args=[client])
send_thread.start()
recv_thread.start()
send_thread.join()

recv_thread.join()

exit(0)