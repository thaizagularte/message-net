import threading
from dataclasses import dataclass, field
from time import sleep
from typing import Optional
from socket import *
from datetime import datetime, timezone


def get_ts() -> str:
    return str(int(datetime.now(tz=timezone.utc).timestamp()))

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
    user: User = field(default_factory=User)
    PORT: int = 19033
    HOST: str = '127.0.0.1'
    socket = socket(AF_INET, SOCK_STREAM)

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

        except Exception as err:
            print(f'Erro ao conectar: {err}')

    def request_register(self):
        try:
            self.socket.send('01'.encode())
        except Exception:
            print('Erro ao Registrar')
            return False

    def register(self, data):
        return self.user.load_id(data)

    def conn_user(self):
        if self.user.id:
            try:
                self.socket.send(f'03{self.user.id}'.encode())
                print('Conectado como', self.user.id)
                return True
            except Exception:
                print('Erro ao Conectar')
                return False
        else:
            print(self.user.id)

    def confirm_recv(self, ):
        pass


    def recv_msg(self, src_id: str, timestamp: float, data: str):
        """
        Método de Recebimento das mensagens enviadas, Argumentos:

        *src_id* ->  Uma sequência de 13 dígitos representando o originador da mensagem\n

        *timestamp* -> Data e hora de envio da mensagem em formato POSIX

        *data* -> Até 218 caractéres de conteúdo que foram enviados
        """

        print(f'New Message Received from {src_id}')
        ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        self.user.add_message(src_id, f'<{ts} | {src_id}> {data}')


    def send_msg(self, dst_id, data) -> bool:
        if len(data) > 218:
            return False

        timestamp = get_ts()
        msg = '05' + self.user.id + dst_id + timestamp + data
        try:
            self.socket.send(msg.encode())
            ts = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            self.user.add_message(dst_id, f'<{ts} | {self.user.id}> {data}')
            return True
        except Exception as e:
            print("erro")
            print(e)
            return False

    def send_seen(self, src_id):
        """
        Método que avisa ao Servidor que o cliente LEU a mensagem recebida

        AÇÃO: notificar servidor que a mensagem RECEBIDA foi lida
        :return:
        """
        timestamp = get_ts()
        try:
            self.socket.send(f'08{src_id}{timestamp}'.encode())
            print()
        except Exception:
            return False


    def recv_seen(self, dst_id : str, timestamp : int):
        """
        Método que avisa ao CLIENTE que a mensagem ENVIADA foi lida

        AÇÃO: notificar cliente
        :return:
        """
        ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Mensagens enviadas para {dst_id} foram lidas às {ts}')

    def create_group(self, members : list):
        timestamp = get_ts()
        members.insert(0, self.user.id)
        members_join = ''.join(members[i] for i in range(len(members)))
        msg = f'10{self.user.id}{timestamp}{members_join}'
        try:
            self.socket.send(msg.encode())
            print('Você criou com sucesso o grupo com os membros:')
            for member in members:
                print(f'{member}')

        except Exception:
            print('Erro ao Conectar')
        




    def handle_recv(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            data = data.decode()
            print(data)
            match data[:2]:
                case '02':
                    self.register(data[2:])
                case '06':
                    print(data)
                    self.recv_msg(src_id=data[2:15], timestamp=int(data[28:38]), data=data[38:])
                case '07':
                    print('confirm send')
                    print(data)
                case '09':
                    print('ALERT')
                    self.recv_seen(dst_id=data[2:15], timestamp=int(data[15:]))
                case '11':    
                    print(f'Servidor criou o grupo id: {data[2:15]}')
                    
                    


    '''

    CLIENT PROTOCOL SEND:
    COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  01 | Try Register in Server                         |  [COD(2)]
[✔]  03 | Try Notify the User is Online                  |  [COD(2)][ID(13)]
[✔]  05 | Try Send a Message to a other User             |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  08 | Try Notify the User is Seen Message Received   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  10 | Try Create a Group                             |
    
    CLIENT PROTOCOL RECEIVE:
   COD |                    ACTION                      |   STRUCTURE
--------|------------------------------------------------|--------------------------------------------------------|
[✔]  02 | Confirm Register and Receive ID                |  [COD(2)][ID(13)]
[✔]  06 | Receive Message                                |  [COD(2)][SRC(13)][DST(13)][TIMESTAMP(10)][MSG(218)]
[✔]  07 | Confirm Send Message                           |  [COD(2)][DST(13)][TIMESTAMP(10)]
[✔]  09 | Receive Seen                                   |  [COD(2)][SRC(13)][TIMESTAMP(10)]
[ ]  11 | Add in a Group                                 |
    '''
