from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie import fields

from books.models import Book, Tag, Person

import json

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

    def obj_get_list(self, bundle, **kwargs):
        if 'taggings' in bundle.request.GET:
            tags =  bundle.request.GET['taggings']
            print tags
            print type(tags)
            tags = json.loads(tags)
            # We need unique tags
            tags = set(tags)
            objs = super(BookResource, self).obj_get_list(bundle, **kwargs)
            new_objs = []
            for o in objs:
                obj_tags = set([t.name for t in o.tags.all()])
                if tags.issubset(obj_tags):
                    new_objs.append(o)
            objs = new_objs
        else:
            objs = super(BookResource, self).obj_get_list(bundle, **kwargs)
        return objs


    class Meta:
        queryset = Book.objects.all()
        resource_name = 'books'
        filtering = {'title': ALL}

