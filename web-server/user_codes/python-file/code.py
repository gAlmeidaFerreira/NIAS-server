import requests
import os
import time

url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png'

nome_arquivo = "Python.png"

diretorio_destino = "/app/output"

caminho_destino = os.path.join(diretorio_destino, nome_arquivo)

response = requests.get(url)

if response.status_code == 200:
    with open(caminho_destino,'wb') as file:
        file.write(response.content)
    print("Imagem salva com sucesso")
    time.sleep(30)
else:
    print("Falha ao baixar a imagem:", requests.status_codes)
