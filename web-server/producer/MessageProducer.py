import pika
import os
from flask import Flask, request, jsonify

# Declarando variáveis
queue_name = os.environ.get('QUEUE_NAME')
broker_name = os.environ.get('BROKER_NAME')
queue_producer_name = os.environ.get('QUEUE_PRODUCER_NAME')
queue_producer_port = os.environ.get('QUEUE_PRODUCER_PORT')

app = Flask(__name__)

#Criando conexão com fila rabbitmq
def QueueConnection(queue_name):
    connection_params = pika.ConnectionParameters(broker_name)

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    
    return channel

# Endpoint para receber arquivo e enviar para fila
@app.route('/product_message', methods=['POST'])
def product_message():
    try:
        file = request.data
        channel = QueueConnection(queue_name=queue_name) # Declarando canal da fila
        channel.basic_publish(exchange='', routing_key=queue_name, body=file) # Enviando conteúdo do arquvio para a fila
        response = jsonify({'message':'Mensagem Enviada para fila com sucesso'})
        response.status_code = 200
        return response

    except Exception as ex:
        response = jsonify({'error': str(ex)})
        response.status_code = 500
        return response

if __name__ == '__main__':
    app.run(host=queue_producer_name, port=queue_producer_port)