import uuid
import pika

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = '5672'
RABBITMQ_USER = 'root'
RABBITMQ_PASS = '1234'

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,
                                       port=RABBITMQ_PORT,
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='tutorial')

for _ in range(20):

    msg = str(uuid.uuid4())
    channel.basic_publish(exchange='', routing_key='tutorial', body=msg)
    print(f' [x] Sent: {msg}')

connection.close()
