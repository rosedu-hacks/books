from django.db import models
from datetime import datetime

class Book(models.Model):
    """Entry for a generic book"""
    title = models.TextField(max_length=100)
    author = models.TextField(max_length=100)

class Tag(models.Model):
    """Available tags that can be put on books"""
    name = models.TextField(max_length=20)
    books = models.ManyToManyField('Book', related_name='tags')

class Person(models.Model):
    name = models.TextField(max_length=20)

    ###Sharing stuff
    shared = models.ManyToManyField('Book', related_name='shared_by')

    ###Books that I rented from others
    reccomended = models.ManyToManyField('Book', through='Reccomendation', related_name='reccomended_by')
    whishlist = models.ManyToManyField('Book', related_name='wished_by')
    read_books = models.ManyToManyField('Book', related_name='read_by')

    def __unicode__(self):
        return self.name

class Rental(models.Model):
    PENDING_SHARE = 0
    ACCEPTED = 1
    PENDING_RETURN = 2
    Status = (
        (PENDING_SHARE, 'PendingShare'),
        (ACCEPTED, 'Accepted'),
        (PENDING_RETURN, 'PendingReturn'))

    status = models.IntegerField(choices=Status, default=PENDING_SHARE)
    by = models.ForeignKey(Person, related_name='rentals_to')
    to = models.ForeignKey(Person, related_name='rentals_from')
    book = models.ForeignKey(Book, related_name='rentals')
    until = models.DateField(default=datetime.now)

class Reccomendation(models.Model):
    by = models.ForeignKey(Person)
    book = models.ForeignKey(Book)
    text = models.TextField(max_length=100)

