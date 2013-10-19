from resources import BookResource
from tastypie.api import Api

v1_api = Api(api_name = 'v1')
v1_api.register(BookResource())
