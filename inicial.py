import tkinter as tk
from tkinter import simpledialog, messagebox


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo de Chat")
        self.geometry("400x300")
        self.frames = {}

        # Adiciona todas as telas ao dicionário frames
        for F in (TelaInicial, MenuPrincipal):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar a Tela Inicial
        self.show_frame("TelaInicial")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#0E1A35")  # Cor de fundo
        self.create_widgets()

    def create_widgets(self):
        # Logotipo
        logo = tk.Label(self, text="CHAT", font=("Helvetica", 24), bg="#0E1A35", fg="white")
        logo.pack(pady=50)

        # Botões
        btn_registrar = tk.Button(self, text="Registrar", command=self.registrar)
        btn_registrar.pack(pady=10)

        btn_conectar = tk.Button(self, text="Conectar", command=self.conectar)
        btn_conectar.pack(pady=10)

    def registrar(self):
        # Exibe popup de carregamento
        messagebox.showinfo("Carregando", "Registrando usuário...")
        self.controller.show_frame("MenuPrincipal")

    def conectar(self):
        # Recebe input do usuário
        user_input = simpledialog.askstring("Conectar", "Digite seu usuário:")
        if user_input:
            messagebox.showinfo("Conectando", f"Bem-vindo, {user_input}!")
            self.controller.show_frame("MenuPrincipal")


class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#0E1A35")  # Cor de fundo
        label = tk.Label(self, text="Menu Principal", font=("Helvetica", 24), bg="#0E1A35", fg="white")
        label.pack(pady=50)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
