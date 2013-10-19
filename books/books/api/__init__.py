from resources import *
from tastypie.api import Api

v1_api = Api(api_name = 'v1')
v1_api.register(BookResource())
v1_api.register(TagResource())
v1_api.register(PersonResource())
