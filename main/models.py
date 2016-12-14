from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
# import uuid
# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    birth_date = models.DateField(null=True)
    # uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return '{} {} - {}'.format(self.name, self.surname, self.birth_date)

    @property
    def full_name(self):
        return '{} {}'.format(self.name, self.surname)

    class Meta:
        unique_together = ('name', 'surname', 'birth_date')


class Book(models.Model):

    title = models.CharField(max_length=100, null=False)
    authors = models.ManyToManyField(Author, related_name='books')
    lc_classification = models.CharField(max_length=32)
    # uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'lc_classification')


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# user.auth_token returns token
