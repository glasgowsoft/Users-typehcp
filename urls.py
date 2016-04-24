#from django.conf             import settings
#from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    # transactions that merely view the database
    url(r'^userlist/$',                                                 views.user_list,                   name='userlist'),
    url(r'^userdetail/(?P<pk>[0-9]+)/$',                                views.user_detail,                 name='userdetail'),
    #
    # transactions that update the database in one stage, using parameters, not forms
    url(r'^unsubscribe/(?P<confirmed>[a-z]*)/',                         views.unsubscribe,                 name='unsubscribe'),
    url(r'^userdelete/(?P<pk>[0-9]+)/(?P<confirmed>[a-z]*)/',           views.user_delete,                 name='userdelete'),
    url(r'^promote/(?P<pk>[0-9]+)/',                                    views.promote,                     name='promote'),
    url(r'^demote/(?P<pk>[0-9]+)/',                                     views.demote,                      name='demote'),
    #
    # transactions that update the database in two stages, using forms
    url(r'^userinsert/$',                                               views.user_insert,                 name='userinsert'),
    url(r'^password/',                                                  views.password,                    name='password'),
    url(r'^displayname/',                                               views.display_name,                name='displayname'),
    url(r'^userupdate/(?P<pk>[0-9]+)/$',                                views.user_update,                 name='userupdate'),
    #
    #url(r'^userupdate/(?P<pk>[0-9]+)/(?P<function>[a-z]+)/$',           views.user_update,                name='userupdate'),
    #url(r'^userinsert/(?P<function>[a-z]+)/$',                          views.user_insert,                 name='userinsert'),
]
