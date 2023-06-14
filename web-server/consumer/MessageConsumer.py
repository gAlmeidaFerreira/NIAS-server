import pika
import socket
import os
import requests

"""
HOST = os.environ.get('PROCESS_UNITY_NAME')     # Endereco IP da unidade de processamento
PORT = int(os.environ.get('PROCESS_UNITY_PORT'))            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
"""

#Criando conexão com fila rabbitmq
def QueueConnection():
    connection_params = pika.ConnectionParameters(os.environ.get('BROKER_NAME'))

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    channel.queue_declare(queue=os.environ.get('QUEUE_NAME'))
    #channel.queue_declare('fila-teste')
    
    return channel


#Criando callback para consumer
def callback(ch, method, properties, body):

    print(f"mensagem recebida")

    #Enviando arquivo para unidade de processamento
    url_processor = f"http://{os.environ.get('PROCESS_UNITY_NAME')}:{os.environ.get('PROCESS_UNITY_PORT')}/process-file"
    response = requests.post(url_processor, data=body)

    if response.status_code == 200:
        ch.basic_ack(delivery_tag=method.delivery_tag) #Processamento bem sucedido
        print("mensagem processada")
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag, requeue=True) #Processamento mal sucedido, enviando mensagem de volta à fila
        print("mensagem não processada, enviando arquivo de volta à fila")


channel = QueueConnection() #Declarando canal
channel.basic_consume(queue=os.environ.get('QUEUE_NAME'), on_message_callback=callback)
#channel.basic_consume(queue='fila-teste', on_message_callback=callback)
channel.start_consuming()
print("consumidor pronto para receber mensagens")