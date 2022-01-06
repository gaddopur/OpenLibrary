import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contentService.settings")
django.setup()

from books.models import Book

params = pika.URLParameters('amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='bookinteraction')


def callback(ch, method, properties, body):
    print('Received in contentService')
    id = json.loads(body)
    print(id)
    try:
        book = Book.objects.get(id=id)
        book.numberOfInteractions = book.numberOfInteractions + 1
        book.save()
        print('Book likes increased!')
    except Book.DoesNotExist:
        print('Interacted book doesnot exist')


channel.basic_consume(queue='bookinteraction', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()