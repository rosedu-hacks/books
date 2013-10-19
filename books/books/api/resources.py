from tastypie.resources import ModelResource
from tastypie import fields

from books.models import Book, Tag, Person

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tags'

class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.all()
        resource_name = 'persons'

class BookResource(ModelResource):
    description = fields.CharField(attribute='description')
    picture_url = fields.CharField(attribute='picture_url')
    rented_by = fields.ListField(attribute='rented_by')

    tags = fields.ToManyField(TagResource, 'tags')
    shared_by = fields.ToManyField(TagResource, 'shared_by')
    reccomended_by = fields.ToManyField(TagResource, 'reccomended_by')

    class Meta:
        queryset = Book.objects.all()
        resource_name = 'books'

