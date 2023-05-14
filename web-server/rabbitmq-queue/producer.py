import pika
import time
import random

# Criando e configurando a conexão
connection_params = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_params)

#Criando o canal
channel = connection.channel()

## Configurando a fila e enviando a mensagem
# Criando a fila
channel.queue_declare(queue="letterbox")

#Loop infinito para simular envio de mensagens por diferentes usuários
mensageId = 1
while(True):

    #Criando a mensagem
    message = f"Enviando Mensagem: {mensageId}"

    #Declarando a exange e enviando a mensagem
    channel.basic_publish(exchange='', routing_key="letterbox", body=message)

    print(f"enviando a mensagem: {message}")

    time.sleep(random.randint(1, 4))

    mensageId += 1


