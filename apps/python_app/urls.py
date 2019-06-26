from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_user$', views.create_user),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^submit_quote$', views.submit),
    url(r'^show_quote/(?P<id>\d+)$', views.show_quote),
    url(r'^add_fave/(?P<quote_id>\d+)$', views.add_fave),
    url(r'^remove_fave/(?P<quote_id>\d+)$', views.remove_fave),
    url(r'^logout$', views.logout)
]