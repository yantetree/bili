from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
        url(r'^search/(?P<ename>[a-zA-Z]+)/$', 'eparser.views.get_price'),
)
