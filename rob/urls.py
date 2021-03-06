from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Additional imports for users:
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^game/(?P<pk>\d+)/$', views.view_game, name='view_game'),
    url(r'^game/(?P<pk>\d+)/selection/(?P<choice>(\w+))/$', views.join_game, name='join_game'),
    url(r'^accounts/register/$',views.register, name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^game/new/$', views.game_new, name='game_new'),
    url(r'^game/(?P<pk>\d+)/remove/$', views.remove_game, name='remove_game'),
    url(r'^game/(?P<pk>\d+)/setstake/$', views.set_stake, name='set_stake'),


]
