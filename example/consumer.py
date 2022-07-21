import time
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

def callback(ch, method, properties, body):

    print(f" [x] Received {body.decode()}")
    channel.basic_ack(method.delivery_tag)
    time.sleep(1)

channel.basic_consume(queue='tutorial', on_message_callback=callback)

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Interrupted.')
    channel.stop_consuming()

connection.close()
