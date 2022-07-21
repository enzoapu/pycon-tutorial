import time
import random
import pika


RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = '5672'
RABBITMQ_USER = 'root'
RABBITMQ_PASS = '1234'

collection_batch_size = 5
collection = []


def run(task):

    sleep_time = random.randint(1,6)
    print('sleep time:', sleep_time, '\n')
    time.sleep(sleep_time)


def batch_run(tasks):

    print('tasks length:', len(tasks))
    print(tasks, '\n')

    rand_num = random.randint(0,10)

    if rand_num == 0:
        print('failed.', '\n')
        return False
    else:
        print(tasks, '\n')
        time.sleep(3)
        return True


def callback(ch, method, properties, body):

    msg = body.decode()
    print(f" [*] Received: {msg}")
    time.sleep(2)

    # run(msg)


def batch_callback(ch, method, properties, body):

    msg = body.decode()
    print(f" [*] Received: {msg}")

    collection.append(msg)
    if len(collection) % collection_batch_size == 0:
        result = batch_run(collection)
        if result:
            ch.basic_ack(delivery_tag = method.delivery_tag, multiple=True)
        else:
            ch.basic_nack(delivery_tag = method.delivery_tag, multiple=True)
        collection.clear()


credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,
                                    port=RABBITMQ_PORT,
                                    credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='work-queue')

# channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='work-queue', on_message_callback=callback)

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print('Stop consuming.')
    channel.stop_consuming()

connection.close()
