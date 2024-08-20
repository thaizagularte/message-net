import threading
from dataclasses import dataclass, field
from time import sleep
from typing import Optional
from socket import *
from datetime import datetime, timezone


@dataclass(slots=True)
class User:
    id: Optional[str] = None
    username: Optional[str] = None
    messsages: dict = field(default_factory=dict)

    def load_id(self, id: str) -> None:
        if not self.id:
            self.id = id
            print(f"User {self.id} loaded")

    def add_message(self, sender, data: str) -> None:
        if sender not in self.messsages.keys():
            self.messsages[sender] = []
        self.messsages[sender].append(data)


@dataclass
class Client:
    user: User = User()
    PORT: int = 2024
    HOST: str = '127.0.0.1'
    socket: socket = socket(AF_INET, SOCK_STREAM)

    def __del__(self):
        self.socket.close()
        print("Socket deletado!")

    def set_host(self, host) -> str:
        self.HOST = host
        return self.HOST

    def load_messages(self, people):
        try:
            for message in self.user.messsages[people]:
                print(message)
        except KeyError:
            return

    def conn_serv(self) -> bool:
        """Método para iniciar uma tentativa de conexão com o servidor"""
        try:
            self.socket.connect((self.HOST, self.PORT))
            print("Conexão Bem-Sucedida!")
            return True
        except Exception as err:
            print(f'Erro ao conectar: {err}')
            return False

    def register(self):
        try:
            self.socket.send('01'.encode())
            return True
        except Exception:
            print('Erro ao Registrar')
            return False

    def conn_user(self):
        print(self.user.id)
        if self.user.id:
            try:
                self.socket.send(f'03{self.user.id}'.encode())
                print(f'Usuário {self.user.id} Conectado!')
                return True
            except Exception:
                print('Erro ao Conectar')
                return False

    def confirm_recv(self, ):
        pass

    def recv_msg(self, src_id: str, timestamp: float, data: str):
        """
        Método de Recebimento das mensagens enviadas, Argumentos:

        *src_id* ->  Uma seq
        uência de 13 dígitos representando o originador da mensagem\n

        *timestamp* -> Data e hora de envio da mensagem em formato POSIX

        *data* -> Até 218 caractéres de conteúdo que foram enviados
        """
        print(f'New Message Received from {src_id}')
        ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self.user.add_message(src_id, f'<{ts} | {src_id}> {data}')

    def send_msg(self, dst_src, data) -> bool:
        if len(data) > 218:
            return False
        timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        msg = '05' + self.user.id + dst_src + str(timestamp) + data
        try:
            self.socket.send(msg.encode())
            ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            self.user.add_message(dst_src, f'<{ts} | {self.user.id}> {data}')
            return True
        except Exception:
            return False

    def handle_recv(self):
        while True:
            data = self.socket.recv(1024)
            data = data.decode()
            print(data)
            match data[:2]:
                case '02':
                    print("Solicitação de Registro concluída!")
                    user_id = data[2:]
                    self.user.load_id(user_id)
                case '06':
                    print(data)
                    self.recv_msg(src_id=data[2:15], timestamp=float(data[15:28]), data=data[28:])
'''
06-2696474255762-2790755052171-1724155138.798417oi
cd___id_src____---id-dst----'''