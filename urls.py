#from django.conf             import settings
#from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    # transactions that merely view the database
    url(r'^memberlist/$',                                                                   views.member_list,                 name='memberlist'),
    url(r'^circlelist/$',                                                                   views.circle_list,                  name='circlelist'),
    url(r'^memberdetail/(?P<pk>[0-9]+)/$',                                                  views.member_detail,               name='memberdetail'),
    url(r'^circledetail/(?P<pk>[0-9]+)/$',                                                  views.circle_detail,                  name='circledetail'),
    #
    # transactions that update the database in one stage, using parameters, not forms
    url(r'^promote/(?P<pk>[0-9]+)/',                                                        views.promote,                     name='promote'),
    url(r'^demote/(?P<pk>[0-9]+)/',                                                         views.demote,                      name='demote'),
    #
    # transactions that update the database in two stages, using parameters, not forms
    url(r'^unsubscribe/(?P<confirmed>[a-z]*)/',                                             views.unsubscribe,                 name='unsubscribe'),
    url(r'^memberdelete/(?P<pk>[0-9]+)/(?P<confirmed>[a-z]*)/',                             views.member_delete,               name='memberdelete'),
    url(r'^circledelete/(?P<pk>[0-9]+)/(?P<confirmed>[a-z]*)/',                             views.circle_delete,               name='circledelete'),
    url(r'^useroptions/(?P<type>[a-z]+)/(?P<color>[#a-zA-Z0-9]+)/(?P<whence>[a-z]+)/$',     views.user_options,                name='useroptions'),
    #
    # transactions that update the database in two stages, using forms
    url(r'^memberinsert/$',                                                                 views.member_insert,               name='memberinsert'),
    url(r'^contactinsert/$',                                                                views.contact_insert,              name='contactinsert'),
    url(r'^circleinsert/$',                                                                 views.circle_insert,               name='circleinsert'),
    url(r'^password/',                                                                      views.password,                    name='password'),
    url(r'^displayname/',                                                                   views.display_name,                name='displayname'),
    url(r'^memberupdate/(?P<pk>[0-9]+)/$',                                                  views.member_amend,                name='memberupdate'),
    url(r'^circleupdate/(?P<pk>[0-9]+)/$',                                                  views.circle_amend,                name='circleupdate'),
    #
]
