from django.contrib import admin

from models import *

admin.site.register(Person)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Rental)
admin.site.register(Reccomendation)
