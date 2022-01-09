# amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq

import pika, json

params = pika.URLParameters('amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq')


def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='user', body=json.dumps(body), properties=properties)
    channel.close()
    connection.close()