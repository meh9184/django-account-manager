from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import deposit_view, withdraw_view, transfer_view

urlpatterns = [
    path('deposit/<account_no>', deposit_view, name='Deposit'),
    path('withdraw/<account_no>', withdraw_view, name='Withdraw'),
    path('transfer/<account_no>', transfer_view, name='Transfer')
]