import pika

# Criando e configurando a conexão
connection_params = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_params)

#Criando o canal
channel = connection.channel()

## Configurando a fila e enviando a mensagem
# Criando a fila
channel.queue_declare(queue="letterbox")

#Criando a mensagem
message = "Hello world! Minha primeira mensagem"

#Declarando a exange e enviando a mensagem
channel.basic_publish(exchange='', routing_key="letterbox", body=message)

print(f"enviando a mensagem: {message}")

#Fechando a conexão
connection.close()


