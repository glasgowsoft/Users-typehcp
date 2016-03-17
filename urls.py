from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^userlist/$',                                                 views.user_list,                   name='userlist'),
    url(r'^userupdate/(?P<pk>[0-9]+)/(?P<function>[a-z]+)/$',           views.user_process,                name='userupdate'),
    url(r'^userinsert/(?P<function>[a-z]+)/$',                          views.user_process,                name='userinsert'),
]
