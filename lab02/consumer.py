import sys
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

channel.exchange_declare(exchange='logs', exchange_type='direct')

result = channel.queue_declare(queue='')
queue_name = result.method.queue


def callback(ch, method, properties, body):

    print(f" [x] Received:  {method.routing_key}  {body.decode()}")


levels = sys.argv[1:]
for level in levels:
    channel.queue_bind(exchange='logs', 
                       queue=queue_name, 
                       routing_key=level)

channel.basic_consume(queue=queue_name, 
                      on_message_callback=callback,
                      auto_ack=True)

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Interrupted.')
    channel.stop_consuming()

connection.close()
