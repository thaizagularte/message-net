from c import *
import threading


def interface():
    t = threading.Thread(target=c.handle_recv)
    t1 = threading.Thread(target=inicio)
    t.start()
    t1.start()
    t.join()
    t1.join()

def menu():
    timeout = 0
    while not c.conn_user():
        sleep(1)
        timeout += 1
        if timeout == 10:
            print('Failed')
            return inicio()
            break


    while True:
        print("### Menu ###")
        choice = input("[1] Mandar mensagem\n[2] Abrir Conversa\nInput: ")
        match choice:
            case "1":
                dst = input("Digite o ID do destino: ")
                msg = input("Digite a mensagem de até 218 caracteres: ")
                c.send_msg(dst, msg)
            case "2":
                contact_id = input('De quem? ')
                c.send_seen(contact_id)
                c.load_messages(contact_id)







def login():
    c.user.load_id(input("Insira o ID: "))
    if not c.conn_user():
        login()
    return



def inicio():

    choice = int(input("### CHAT ###\n[0] Registrar\n[1] Login\n[2] Exit\nInput:"))
    match choice:
        case 0:
            c.request_register()
            menu()
        case 1:
            login()
            menu()
        case 2:
            return

c = Client()
c.conn_serv()
interface()



