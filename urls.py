from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                      views.event_list),
    url(r'^event/list/(?P<periodsought>[a-z]+)/$',                  views.event_list,                   name='event_list'),
    url(r'^event/process/(?P<function>[a-z]+)/$',                   views.event_process,                name='event_insert'),
    url(r'^event/process/(?P<function>[a-z]+)/(?P<pk>[0-9]+)/$',    views.event_process,                name='event_process'),
    url(r'^12345diary12345/$',                                      views.events_hardcoded,             name='events_hardcoded'),
    url(r'^person/list/$',                                          views.person_list,                  name='person_list'),
    url(r'^person/process/(?P<function>[a-z]+)/$',                  views.person_process,               name='person_insert'),
    url(r'^person/process/(?P<function>[a-z]+)/(?P<pk>[0-9]+)/$',   views.person_process,               name='person_process'),
    url(r'^circle/list/$',                                          views.circle_list,                  name='circle_list'),
    url(r'^circle/process/(?P<function>[a-z]+)/$',                  views.circle_process,               name='circle_insert'),
    url(r'^circle/process/(?P<function>[a-z]+)/(?P<pk>[0-9]+)/$',   views.circle_process,               name='circle_process'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

