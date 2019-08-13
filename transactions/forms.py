from django import forms

from .models import Deposit, Withdraw, Transfer

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["account_no", "account_bank", "amount"]

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["account_no", "account_bank", "amount"]
    
    # Validation has to be done

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["account_bank_to", "account_no_to", "account_bank_from", "account_no_from", "amount"]