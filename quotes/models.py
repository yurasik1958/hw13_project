from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.CharField(max_length=30)
    born_location = models.CharField(max_length=120)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


