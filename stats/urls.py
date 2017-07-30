from django.conf.urls import url
from stats import views

urlpatterns = [
    url(r'^$', views.statistics, name='statistics'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.user_register, name='user_registration'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9@.]+)$', views.get_user_profile),
    url(r'^client/(?P<client_number>[0-9]+)$', views.get_client_info),

    # Edit URLs
    url(r'^edit-client/(?P<pk>[0\w-]+)$', views.ClientUpdate.as_view(), name='edit_client'),
    url(r'^edit-abuse/(?P<pk>[0\w-]+)$', views.AbuseUpdate.as_view(), name='edit_abuse'),
    url(r'^edit-situation/(?P<pk>[0\w-]+)$', views.SituationUpdate.as_view(), name='edit_situation'),
    url(r'^edit-service/(?P<pk>[0\w-]+)$', views.ServiceUpdate.as_view(), name='edit_service'),
    url(r'^edit-referral/(?P<pk>[0\w-]+)$', views.ReferralUpdate.as_view(), name='edit_referral'),

    url(r'^data/$', views.data, name='data'),
    url(r'^form/?$', views.form, name='form'),
    url(r'^clients/$', views.clients, name='clients'),
    url(r'^invite_key$', views.invite_key),
]
