from django.db import models

# Create your models here.

class Message(models.Model):
    source = models.CharField(max_length=60)
    to = models.CharField(max_length=60)
    body = models.TextField()

    def __str__(self):
        return self.source + " -> " + self.to + " : " + self.body