from django.db import models

class Question(models.Model):
    text=models.CharField(max_length=255)
    fields=models.CharField(max_length=255)

    def __str__(self):
        return self.text