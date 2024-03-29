import pika
import os
import requests

# Declarando variáveis
queue_name = os.environ.get('QUEUE_NAME')
broker_name = os.environ.get('BROKER_NAME')
process_unity_name = os.environ.get('PROCESS_UNITY_NAME')
process_unity_port = os.environ.get('PROCESS_UNITY_PORT')
processor_url = f"http://{process_unity_name}:{process_unity_port}/process_file"

#Criando conexão com fila rabbitmq
def QueueConnection(queue_name):
    connection_params = pika.ConnectionParameters(broker_name)

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    #channel.queue_declare('fila-teste')
    
    return channel

#TODO: #5 Adicionar política de retentativa no caso de retorno de mensagem para fila

#Criando callback para consumer
def callback(ch, method, properties, body):

    print(f"mensagem recebida")

    #Enviando arquivo para unidade de processamento
    response = requests.post(processor_url, data=body)

    if response.status_code == 200:
        ch.basic_ack(delivery_tag=method.delivery_tag) #Processamento bem sucedido
        print(response.json())
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) #Processamento mal sucedido, enviando mensagem de volta à fila
        print(response.json())
        


channel = QueueConnection(queue_name=queue_name) #Declarando canal
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
print("consumidor pronto para receber mensagens")