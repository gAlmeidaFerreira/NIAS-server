#!/usr/bin/python3

import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

print('Para sair digite bye\n')
try:
    while True:
        msg = input()
        tcp.send (msg.encode())
        if msg=='bye':
            break
finally:
    tcp.close()
