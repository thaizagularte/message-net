from tkinter import Tk
from gui.initial_screen import create_initial_screen
from c import Client


def main():
    client = Client()
    client.conn_serv()
    root = Tk()
    root.title("Aplicativo Chat")
    root.geometry("800x600")
    root.configure(bg='#0b1736')

    create_initial_screen(root, client)

    root.mainloop()

if __name__ == "__main__":
    main()
