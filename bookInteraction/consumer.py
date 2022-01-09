import pika, json, os, django, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookInteraction.settings")
django.setup()

from django.db import connection as dbcon
from userbook.models import User, Book


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

def worker(queue_name):
    while not checkTableExists('userbook_user') and not checkTableExists('userbook_book'):
        print("Migration is not completed!")
        time.sleep(0.5)
    
    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    
    def callback(ch, method, properties, body):
        print('Received in userinteraction')
        id = json.loads(body)
        if properties.content_type == queue_name + '_created':
            if queue_name == 'user':
                instance = User(userid=id)
            elif queue_name == 'book':
                instance = Book(bookid=id)
            instance.save()

        elif properties.content_type == queue_name + '_deleted':
            if queue_name == 'user':
                instance = User.objects.get(userid=id)
            elif queue_name == 'book':
                instance = Book.objects.get(bookid=id)
            instance.delete()

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Started Consuming')

    channel.start_consuming()

    channel.close()
