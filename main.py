import socket
from server import init_server
HOST= '127.0.0.1'
PORT=2000
s = init_server()
s.bind((HOST, PORT))
s.listen(5)
s.accept()
