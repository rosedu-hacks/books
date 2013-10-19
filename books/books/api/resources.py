from tastypie.resources import ModelResource
from tastypie.constants import ALL
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
    rented_by = fields.ToManyField(PersonResource,
                                   attribute=lambda bundle: bundle.obj.rented_by,
                                   null=True, blank=True)

    tags = fields.ToManyField(TagResource, 'tags')
    shared_by = fields.ToManyField(PersonResource, 'shared_by')
    reccomended_by = fields.ToManyField(PersonResource, 'reccomended_by')



    class Meta:
        queryset = Book.objects.all()
        resource_name = 'books'
        filtering = {'title': ALL}

