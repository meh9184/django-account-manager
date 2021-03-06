"""django-account-manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from transactions.views import transcations_detail, transcations_summary, transcations_timeline
from users.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', account_view),
    path('accounts/modify_main', account_modify_main),
    path('accounts/history/<account_no>', account_history),
    path('accounts/history_all/', account_history_all),
    path('accounts/delete/<account_no>', account_delete),
    path('accounts/proc/<account_no>', account_proc),
    path('accounts/detail/<account_no>', account_detail),
    path('transactions/', include('transactions.urls')),
    path('transactions/timeline/', transcations_timeline),
    path('users/', include('django.contrib.auth.urls')),
    # path('balance/',TemplateView.as_view(template_name='check_bal.htm'),name='check Bal'),

]
