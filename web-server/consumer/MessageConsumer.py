import pika
import socket
import os


HOST = os.environ.get('PROCESS_UNITY_NAME')     # Endereco IP da unidade de processamento
PORT = int(os.environ.get('PROCESS_UNITY_PORT'))            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


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

    print(f"mensagem {body} recebida")

    
    #Enviando arquivo para unidade de
    try:
        while True:
            msg = body
            tcp.sendall(msg)
            if not msg:
                print("Falha ao enviar mensagem para unidade de processamento")
                break
    finally:
        tcp.close()
    
    
    #Confirmando processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("mensagem processada")

channel = QueueConnection() #Declarando canal
channel.basic_consume(queue=os.environ.get('QUEUE_NAME'), on_message_callback=callback)
#channel.basic_consume(queue='fila-teste', on_message_callback=callback)
channel.start_consuming()
print("consumidor pronto para receber mensagens")