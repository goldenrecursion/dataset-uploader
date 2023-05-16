from django.urls import path
from django.views.generic.base import RedirectView

from . import views 

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='moralis_auth'), name='auth'),
    path('moralis_auth', views.moralis_auth, name='moralis_auth'),
    path('request_message', views.request_message, name='request_message'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('verify_message', views.verify_message, name='verify_message'),
]
