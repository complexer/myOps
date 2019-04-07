from django.db import models

class Repo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.name