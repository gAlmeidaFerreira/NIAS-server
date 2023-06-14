import subprocess
import os
import zipfile
from flask import Flask, request, jsonify

app = Flask(__name__)

# Criando processo para executar código do usuário
def code_exec(bash_script):
	process = subprocess.Popen(["bash", "-c", bash_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	if process.returncode != 0:
		print('Erro:', stderr.decode())
	else:
		print('Saída:', stdout.decode())
	return stdout, stderr

#TODO: #1 Pensar em lógica para não depender (ou usar) do nome do arquivo dado pelo usuário
#TODO: #3 Adicionar lógica para que Output dos códigos do susuários não se sobreescrevam
#Criando comando bash para executar código do usuário
bash_script = ''' 
#!/bin/bash

cd /app/user_file/python_file

pip install -r requirements.txt
python3 code.py
'''

extract_path = '/app/user_file'
zip_path = '/app/user_file.zip'

@app.route('/process-file', methods=['POST'])
def process_file():
	
    user_file = request.data
	
    # Recebe arquivo compactado do usuário
    zip_path = '/app/user_file.zip'
    with open(zip_path, 'wb') as file:
        file.write(user_file)
    print("Arquivo recebido")

    # Extrai o arquivo zip
    extract_path = '/app/user_file'
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Arquivo exraído para pasta de execução")

    try:
          stdout, stderr = code_exec(bash_script) # Executando arquivo

          os.remove(zip_path)

          return stdout, 200
    except Exception as ex:
          return jsonify({'error': str(ex)}), stderr, 500
    
if __name__ == '__main__':
    app.run(host=os.environ.get('PROCESS_UNITY_NAME'), port=os.environ.get('PROCESS_UNITY_PORT'))


