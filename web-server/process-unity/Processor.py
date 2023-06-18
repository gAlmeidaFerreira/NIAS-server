import subprocess
import os
import shutil
import zipfile
from flask import Flask, request, jsonify

#Declarando variáveis
process_unity_name = os.environ.get('PROCESS_UNITY_NAME')
process_unity_port = os.environ.get('PROCESS_UNITY_PORT')
extract_path = '/app/user_file'
zip_path = '/app/user_file.zip'

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


#Criando comando bash para executar código do usuário
bash_script = ''' 
#!/bin/bash

file_name=$(echo $(ls /app/user_file))

cd /app/user_file/$file_name

pip install -r requirements.txt
python3 code.py

cd /app

output_origin="/app/user_file/$file_name/output"
output_destiny="/app/output"
output_name="output_$file_name"

mkdir "$output_destiny"
cp -r "$output_origin" "$output_destiny/$output_name"
'''

@app.route('/process_file', methods=['POST'])
def process_file():
	
    user_file = request.data
	
    # Recebe arquivo compactado do usuário
    with open(zip_path, 'wb') as file:
        file.write(user_file)
    print("Arquivo recebido")

    # Extrai o arquivo zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Arquivo exraído para pasta de execução")

    try:
          stdout, stderr = code_exec(bash_script) # Executando arquivo

          os.remove(zip_path)
          shutil.rmtree(extract_path)

          response = jsonify({'message':'Arquivo processado com sucesso', 'code':f'{stdout}'})
          response.status_code = 200
          return response
    
    except Exception as ex:        
          response = jsonify({'error': str(ex), 'error_code':f'{stderr}'})
          response.status_code = 500
          return response
    
if __name__ == '__main__':
    app.run(host=process_unity_name, port=process_unity_port)


