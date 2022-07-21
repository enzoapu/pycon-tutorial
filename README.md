# pycon-tutorial

## Setup
Clone the tutorial repository
```
git clone https://github.com/enzoapu/pycon-tutorial.git
```

### Build RabbitMQ server
use docker
```
# create and start container
docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=root -e RABBITMQ_DEFAULT_PASS=1234 rabbitmq:management

# stop and shutdown container
docker stop rabbitmq

# list containers
docker ps
```

use docker compose
```
# create and start container
docker-compose up

# stop and shutdown container
docker-compose stop
```



### RabbitMQ client library
Install [pika](https://github.com/pika/pika) in your python environment.
```
pip install pika
```

## Run

### Example
```
python example/producer.py
python example/consumer.py
```

### Lab 01
```
python lab01/producer.py
python lab01/consumer.py
```

### Lab 02
```
python lab02/producer.py 
python lab02/consumer.py [info] [warning] [error]
python lab02/consumer.py error > error.log
```
