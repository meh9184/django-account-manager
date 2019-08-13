from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import CustomUser, Account
from .managers import CustomUserManager

from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'full_name', 'mobile_no', 'loc',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'mobile_no', 'loc','balance',)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["account_no", "balance", "bank", "account_type", "is_main_account"]