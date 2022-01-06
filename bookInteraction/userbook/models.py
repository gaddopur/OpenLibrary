from django.db import models

class User(models.Model):
    userid = models.IntegerField(unique=True)

class BookUser(models.Model):
    userid = models.IntegerField()
    bookid = models.IntegerField()
    read = models.BooleanField(default=False)
    like = models.BooleanField(default=False)