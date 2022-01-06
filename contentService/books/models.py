from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    story = models.TextField()
    author = models.IntegerField()
    numberOfInteractions = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)