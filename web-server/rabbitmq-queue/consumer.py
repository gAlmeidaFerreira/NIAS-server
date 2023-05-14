import pika
import time
import random

# Criando call back para indicar quando mensagem foi consumida
def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)

    print(f"Mensagem recebida: {body}, enquanto levará {processing_time} para mensgagem ser processada")
    
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)# Indicando que mensagem terminou de ser consumida
    
    print("Mensagem terminou de ser processada")

## Craindo conexão e declarando a fila
connection_params = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

channel.queue_declare(queue="letterbox")

# Indicando que cada consumidor processará apenas uma mensagem por vez
channel.basic_qos(prefetch_count=1) 

## Configurando o consumo

channel.basic_consume(queue="letterbox", on_message_callback=on_message_received)

print("Começando a consumir")

channel.start_consuming()