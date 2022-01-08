# amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq

import pika, json

params = pika.URLParameters('amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq')
connection = pika.BlockingConnection(params)

def publish(method, body):
    channel = connection.channel()

    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='bookinteraction', body=json.dumps(body), properties=properties)
    channel.close()