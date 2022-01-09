import pika, json, os, django, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contentService.settings")
django.setup()

from django.db import connection as dbcon
from books.models import Book

params = pika.URLParameters('amqps://einowjtq:BFYTVe9jVHse4IBBQIRq_R6l9EnsJwxU@chimpanzee.rmq.cloudamqp.com/einowjtq')

def checkTableExists(table):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{}'
        """.format(table))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

while not checkTableExists('books_book'):
    print("Migration is not competed!")
    time.sleep(0.5)

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