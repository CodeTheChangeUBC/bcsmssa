from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.statistics, name='statistics'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.user_register, name='user_registration'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'profile/(?P<username>[a-zA-Z0-9@.]+)$', views.get_user_profile),
    url(r'client/(?P<client_number>[0-9]+)$', views.get_client_info),
    url(r'^data/$', views.data, name='data'),
    url(r'^form/?$', views.form, name='form'),
    url(r'^invite_key$', views.invite_key),
]
