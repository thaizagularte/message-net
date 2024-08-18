import threading
from socket import *
from time import sleep

HOST = '127.0.0.1'
PORT = 20022


def send_msg(c, u):
    while True:
        try:
            msg = input("Input: ")
            c.send(f'<{u}> {msg}'.encode('utf-8'))
        except Exception as e:
            print(e)
            return




print("### CHAT ###")

user = input("Insira o seu nome para inicar a conexão: ")
client = socket(AF_INET, SOCK_STREAM)

print("Iniciando Conexão")

try:
    client.connect((HOST, PORT))
    print(f'Conectado como {user}!')
except:
    print("Erro ao conectar\nSaindo", end="")
    exit(0)
send_thread = threading.Thread(target=send_msg, args=[client, user])
send_thread.start()
send_thread.join()

exit(0)