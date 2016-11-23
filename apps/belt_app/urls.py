from django.conf.urls import url
from . import views     
     
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^home$', views.home, name="home"),
    url(r'^user/(?P<user_id>\d+)$', views.show_user, name="user"),
    url(r'^friendships/(?P<friendid>\d+)$', views.friendships, name="friendships"),
    url(r'^remove/(?P<friendid>\d+)$', views.remove_asfriend, name="remove")
    ]