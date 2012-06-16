from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('users.views',
    (r'^login/$', 'login'),
    (r'^signup/$', 'signup'),
    (r'^welcome/$', 'welcome'),
    (r'^logout/$', 'logout'),
    (r'^recover/$', 'recover'),
)
