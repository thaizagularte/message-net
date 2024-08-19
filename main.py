from c import *
import threading


def interface():
    t = threading.Thread(target=c.handle_recv)
    t1 = threading.Thread(target=menu)
    t.start()
    t1.start()
    t.join()
    t1.join()

def menu():
    c.conn_user()
    while True:
        print("### Menu ###")
        choice = input("[1] Mandar mensagem\n[2] Abrir Conversa\nInput: ")
        match choice:
            case "1":
                dst = input("Digite o ID do destino: ")
                msg = input("Digite a mensagem de até 218 caracteres: ")
                c.send_msg(dst, msg)
            case "2":

                c.load_messages(input('De quem? '))


c = Client()
c.conn_serv()


def login():
    c.user.load_id(input("Insira o ID: "))
    if not c.conn_user():
        login()
    return



def inicio():
    choice = int(input("### CHAT ###\n[0] Registrar\n[1] Login\n[2] Exit\nInput:"))
    match choice:
        case 0:
            c.register()
            c.conn_user()
            interface()
        case 1:
            login()
            interface()
        case 2:
            return

inicio()


