import time
import random
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

logs = [
    'This is an INFO message.',
    'This is a WARNING message.',
    'This is an ERROR message.'
]
log_list = [random.choice(logs) for _ in range(20)]

for i, log in enumerate(log_list):

    msg = f'({i}){log}'
    
    if 'INFO' in msg:
        channel.basic_publish(exchange='logs', routing_key='info', body=msg)
    if 'WARNING' in msg:
        channel.basic_publish(exchange='logs', routing_key='warning', body=msg)
    if 'ERROR' in msg:
        channel.basic_publish(exchange='logs', routing_key='error', body=msg)
    
    print(f' [x] Sent: {msg}')
    time.sleep(0.5)

connection.close()
