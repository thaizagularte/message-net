from dataclasses import dataclass, field
from datetime import datetime
from random import randint
from socket import *
from typing import Optional, List
import threading

ID_LEN = 13


@dataclass(slots=True)
class Server:
    HOST: Optional[str] = '127.0.0.1'
    PORT: int = 2024
    users: dict = field(default_factory=dict)
    online: List[socket] = field(default_factory=list)
    server: socket = socket(AF_INET, SOCK_STREAM)

    def __del__(self):
        """Método da classe para fehcar o soquete adequadamente ao ser deletado"""
        self.server.close()

        print('Server closed')

    def run(self):
        """Método que roda o servidor e o deixa escutando novas conexões com vários clientes"""
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        print("Servidor Aberto para Conexões")
        try:
            while True:
                try:
                    client, addr = self.server.accept()
                    print(f'Conexão estabelecida com {client.getpeername()}')
                    t_listen = threading.Thread(target=self.listen_client, args=[client])
                    t_listen.start()
                except OSError as e:
                    print(f"Erro de rede: {e}")
                except Exception as e:
                    print(f"Erro inesperado: {e}")
        except KeyboardInterrupt:
            print("Servidor interrompido manualmente.")
        finally:
            self.__del__()  # ou `self.server.close()`

    def listen_client(self, client: socket):
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    print(f'Client {client.getpeername()} disconnected')
                    self.online.remove(client)
                    client.close()
                    break
                self.handle_request(client, data.decode())
                print(f'Client {client.getsockname()} send: {data.decode()}')
            except:
                break

    def register_user(self):
        while True:
            user_id = '2' + ''.join(str(randint(0, 9)) for _ in range(1, ID_LEN))
            if user_id not in self.users:
                self.users[user_id] = 'off'
                break
        print(f'User {user_id} registered')
        return user_id

    def user_online(self, client: socket, user_id: str):
        try:
            self.users[user_id] = client
            self.online.append(client)
            print(f'User {user_id} online')
        except Exception:
            print('User not in Users')

    def forward_msg(self, src_id: str, dst_id: str, timestamp: str, data: str):
        dst_client = self.users[dst_id]
        if dst_client in self.online:
            msg = f'06{src_id}{dst_id}{str(timestamp)}{data}'
            try:
                dst_client.send(msg.encode())
            except:
                return False

    def confirm_rcv(self, src_id, dst_id):
        msg = f'07{dst_id}{datetime.now().timestamp()}'
        try:
            self.users[src_id].send(msg.encode())
        except Exception as e:
            print(f'Erro ao confirmar recebimento: {e}')

    def handle_request(self, client: socket, data: str):
        match (data[:2]):
            case '01':
                user_id = self.register_user()
                return client.send(f'02{user_id}'.encode())
            case '03':
                return self.user_online(client, data[2:])
            case '05':
                return self.forward_msg(src_id=data[2:15], dst_id=data[15:28], timestamp=data[28:38], data=data[38:])


s = Server()
s.run()
