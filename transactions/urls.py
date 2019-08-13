from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import deposit_view, withdraw_view, transfer_view

urlpatterns = [
    path('deposit/', deposit_view, name='Deposit'),
    path('withdraw/', withdraw_view, name='Withdraw'),
    path('tranfer/', transfer_view, name='Transfer')
]