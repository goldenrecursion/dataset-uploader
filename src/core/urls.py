from django.urls import path, include 
from django.views.generic.base import RedirectView

from . import views 

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='index')),
    path('index', views.index, name='index'), 
    path('upload_page', views.upload_page, name='upload_page'),
    path('authenticate_godel', views.authenticate_godel_with_signature, name="auth_godel"),
    path('update_user_jwt', views.update_user_jwt, name="update_user_jwt"),
    path('check_jwt_validity', views.check_jwt_validity, name="check_jwt_validity"),
]