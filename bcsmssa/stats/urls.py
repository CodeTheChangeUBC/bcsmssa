from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.user_register, name='user_registration'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^form/$', views.form, name='form'),
    url(r'^invite_key$', views.invite_key),
]
