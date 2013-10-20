from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Book(models.Model):
    """Entry for a generic book"""
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    @property
    def rented_by(self):
        """Return the persons who rented the current book"""
        rentals = self.rentals.all()
        pks = [r.to.pk for r in rentals]
        return Person.objects.filter(pk__in=pks)

class Tag(models.Model):
    """Available tags that can be put on books"""
    name = models.CharField(max_length=20)
    books = models.ManyToManyField('Book', related_name='tags', null=True, blank=True)

class Person(User):
    ###Sharing stuff
    shared = models.ManyToManyField('Book', related_name='shared_by')

    ###Books that I rented from others
    reccomended = models.ManyToManyField('Book', through='Reccomendation',
                                         related_name='reccomended_by',
                                         null=True, blank=True)
    whishlist = models.ManyToManyField('Book', related_name='wished_by',
                                       null=True, blank=True)
    read_books = models.ManyToManyField('Book', related_name='read_by',
                                        null=True, blank=True)

    @property
    def name(self):
        return " ".join([self.first_name, self.last_name])

    def tag_names(self):
        return [t.name for t in self.tags.all()]

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
    text = models.TextField(max_length=500)

