import socket
import subprocess
import os

# Criando processo para executar código do usuário
def code_exec(bash_script):
	process = subprocess.Popen(["bash", "-c", bash_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	if process.returncode != 0:
		print('Erro:', stderr.decode())
	else:
		print('Saída:', stdout.decode())
	return stdout, stderr

#Criando comando bash para executar código do usuário
bash_script = ''' 
#!/bin/bash

python3 user_code.py
'''

HOST = ''              # Endereco IP do Servidor
PORT = os.environ.get('PROCESS-UNITY_PORT')            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(5)

try:
	while True:
		try:
			connection, cliente = tcp.accept()
			print('Concetado por', cliente)
			file = open("user_code.py", 'wb')
			while True:
				data = connection.recv(1024).decode()
				if not data:
					break
				file.write(data)
				stdout, stderr = code_exec(bash_script)
			print('Finalizando conexao do cliente', cliente)
		except Exception as ex:
			print(ex)
		finally:
			connection.close()
finally:
	tcp.close()