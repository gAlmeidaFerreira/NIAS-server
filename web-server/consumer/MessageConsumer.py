import pika

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

    #Salvando arquvio em diretório local
    with open('/home/guilherme/NIAS/NIAS-server/web-server/frontend-flask/static/files/test_server.txt', 'wb') as arquive:
        arquive.write(body)
    
    #Confirmando recebimento de mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("mensagem processada")

channel = QueueConnection() #Declarando canal
channel.basic_consume(queue='Server-Queue-test', on_message_callback=callback)
channel.start_consuming()
print("consumidor pronto para receber mensagens")