from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^form/$', views.form, name='form'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^new_invite_key$', views.new_invite_key)
]
