from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^form/$', views.form, name='form'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^invite_key$', views.invite_key),
    url(r'^register$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
]
