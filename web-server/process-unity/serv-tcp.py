import socket
import subprocess
import os
import zipfile

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

cd /app/user_file

pip install -r requirements.txt
python3 code.py
'''

HOST = ''              # Endereco IP do Servidor
PORT = int(os.environ.get('PROCESS_UNITY_PORT'))            # Porta que o Servidor esta

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

			zip_path = "/app/user_file.zip"
			with open(zip_path, 'wb') as file: # Salvando arquivo compactado
				data = connection.recv(1024)
				file.write(data)
			print("Arquivo recebido com sucesso")

			extract_path = "/app/user_file"
			with zipfile.ZipFile(zip_path, 'wb') as zip: # Extraindo arquivo compactado
				zip.extractall(extract_path)
			print("Arquivo extraído com sucesso")
				
			stdout, stderr = code_exec(bash_script) # Executando arquivo
			print("Arquvio executado com sucesso")
			print('Finalizando conexao do cliente', cliente)

		except Exception as ex:
			print(ex)
		
		connection.close()
finally:
	tcp.close()