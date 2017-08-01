from django.conf.urls import url
from stats import views

urlpatterns = [
    url(r'^$', views.statistics, name='statistics'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.user_register, name='user_registration'),
    
    # Edit URLs
    url(r'^edit-client/(?P<pk>[0\w-]+)$', views.ClientUpdate.as_view(), name='edit_client'),
    url(r'^edit-abuse/(?P<pk>[0\w-]+)$', views.AbuseUpdate.as_view(), name='edit_abuse'),
    url(r'^edit-situation/(?P<pk>[0\w-]+)$', views.SituationUpdate.as_view(), name='edit_situation'),
    url(r'^edit-service/(?P<pk>[0\w-]+)$', views.ServiceUpdate.as_view(), name='edit_service'),
    url(r'^edit-referral/(?P<pk>[0\w-]+)$', views.ReferralUpdate.as_view(), name='edit_referral'),

    # User profiles
    url(r'^profile/(?P<pk>[0\w-]+)$', views.UserProfile.as_view(), name='user_show'),

    url(r'^data/$', views.data, name='data'),
    url(r'^form/?$', views.form, name='form'),
    url(r'^clients/$', views.clients, name='clients'),
    url(r'^invite_key$', views.invite_key),
]
