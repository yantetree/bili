from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
        url(r'^search/a/$', 'eparser.views.get_single_price'),
        url(r'^search/(?P<ename>[a-zA-Z]+)/$', 'eparser.views.get_price'),
#        url(r'^search/$', 'eparser.views.get_mul_price'),
)
