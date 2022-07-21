import time
import random
import pika


RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = '5672'
RABBITMQ_USER = 'root'
RABBITMQ_PASS = '1234'

collection_batch_size = 3
collection = []

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,
                                    port=RABBITMQ_PORT,
                                    credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='work-queue')


def run(task):

    sleep_time = random.randint(1,6)
    print('sleep time:', sleep_time, '\n')
    time.sleep(sleep_time)


def batch_run(collection):

    print('tasks length:', len(collection))

    rand_num = random.randint(0,10)

    if rand_num == 0:
        print('failed.', '\n')
        return False
    else:
        print(collection, '\n')
        time.sleep(3)
        return True


def callback(ch, method, properties, body):

    msg = body.decode()
    print(f" [*] Received: {msg}")
    # time.sleep(2)
    # run(msg)
    # ch.basic_ack(delivery_tag = method.delivery_tag)

    # batch process
    collection.append(msg)
    if len(collection) % collection_batch_size == 0:
        result = batch_run(collection)
        if result:
            ch.basic_ack(delivery_tag = method.delivery_tag, multiple=True)
        else:
            ch.basic_nack(delivery_tag = method.delivery_tag, multiple=True)
        collection.clear()
        

def consume3():

    inactivity_timeout_count = 0
    last_delivery_tag = 0

    channel.basic_qos(prefetch_count=collection_batch_size)
    
    for method, properties, body  in channel.consume(queue='work-queue', inactivity_timeout=10):
        
        if method == None and properties == None and body == None:

            if len(collection):
                result = batch_run(collection)
                if result:
                    channel.basic_ack(delivery_tag = last_delivery_tag, multiple=True)
                else:
                    channel.basic_nack(delivery_tag = last_delivery_tag, multiple=True)
                collection.clear()
            else:
                print('Queue is inactive.')
                inactivity_timeout_count += 1
                if inactivity_timeout_count == 6:
                    print('Stop consuming.')
                    break
        else:
            last_delivery_tag = method.delivery_tag
            msg = body.decode()
            print(f"[v] Received: {msg}")
            inactivity_timeout_count = 0
            collection.append(msg)
            if len(collection) == collection_batch_size:
                result = batch_run(collection)
                if result:
                    channel.basic_ack(delivery_tag = last_delivery_tag, multiple=True)
                else:
                    channel.basic_nack(delivery_tag = last_delivery_tag, multiple=True)
                collection.clear()

    connection.close()


def consume2():

    # channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='work-queue', on_message_callback=callback)

    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Stop consuming.')
        channel.stop_consuming()

    connection.close()


consume2()