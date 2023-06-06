import pika
import socket

HOST = '127.0.0.1'     # Endereco IP da unidade de processamento
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

#Criando conexão com fila rabbitmq
def QueueConnection():
    connection_params = pika.ConnectionParameters("localhost")

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    channel.queue_declare(queue="Server-Queue-test")
    
    return channel


#Criando callback para consumer
def callback(ch, method, properties, body):

    print(f"mensagem {body} recebida")

    #Enviando arquivo para unidade de
    try:
        while True:
            msg = body
            tcp.send (msg.encode())
            if not msg:
                print("Falha ao enviar mensagem para unidade de processamento")
                break
    finally:
        tcp.close()
    
    #Confirmando processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("mensagem processada")

channel = QueueConnection() #Declarando canal
channel.basic_consume(queue='Server-Queue-test', on_message_callback=callback)
channel.start_consuming()
print("consumidor pronto para receber mensagens")