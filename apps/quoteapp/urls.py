from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^addquote$', views.addquote),
    url(r'^add/(?P<quote_id>\d+)/(?P<user_id>\d+)$', views.addFavorite),
    url(r'^remove/(?P<quote_id>\d+)/(?P<user_id>\d+)$', views.removeFavorite),
    url(r'^users/(?P<user_id>\d+)$', views.users),
]
