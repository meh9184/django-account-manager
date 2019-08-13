from django.urls import path
from . import views
from django.conf.urls import url, include


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('change-pass/', views.change_password),    
]
