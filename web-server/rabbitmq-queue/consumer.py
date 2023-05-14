import pika

# Criando call back para indicar quando mensagem foi consumida
def on_message_received(ch, method, properties, body):
    print(f"Mensagem recebida: {body}") 

## Craindo conexão e declarando a fila
connection_params = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

channel.queue_declare(queue="letterbox")

## Configurando o consumo

channel.basic_consume(queue="letterbox", auto_ack=True, on_message_callback=on_message_received)

print("Começando a consumir")

channel.start_consuming()