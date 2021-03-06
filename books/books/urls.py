from django.conf.urls import patterns, include, url
from django.contrib import admin

from books.api import v1_api

from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'books.views.home', name='home'),
    # url(r'^books/', include('books.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', Overview.as_view(), name='overview'),
    url(r'^register', Register.as_view(), name='register'),
    url(r'^profile/(?P<pk>\d+)/$', Profile.as_view(), name='profile'),
    url(r'^book/(?P<pk>\d+)/$', BookView.as_view(), name='book'),
    url(r'^getbook/(?P<pk>\d+)/$', GetBookView.as_view(), name='getbook'),
    url(r'^editbook/(?P<pk>\d+)/$', EditBookView.as_view(), name='editbook'),
    url(r'^accept_decline/(?P<pk>\d+)/$', accept_decline_view, name='accept_decline'),
    url(r'^accept_return/(?P<pk>\d+)/$', accept_return_view, name='accept_return'),
    url(r'^sharing/(?P<pk>\d+)/$', sharing_view, name='sharing'),
    url(r'login/', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^recc/(?P<pk>\d+)/$', ReccomandationView.as_view(), name='recc'),
    url(r'^addbook', AddBookView.as_view(), name='addbook'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
