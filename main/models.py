from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class Book(models.Model):

    title = models.CharField(max_length=100, null=False)
    authors = models.ManyToManyField(Author, related_name='books')
    lc_classification = models.CharField(max_length=32)

    def __str__(self):
        return self.title


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# user.auth_token returns token
