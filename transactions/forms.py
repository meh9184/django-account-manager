from django import forms

from .models import Deposit, Withdraw, Transfer
from users.models import CustomUser, Account

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["account_bank", "account_no", "amount"]

    def __init__(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')
        super(DepositForm, self).__init__(*args, **kwargs)

        self.fields["account_no"].initial  = account_no
        self.fields["account_bank"].initial  = Account.objects.get(account_no=account_no).bank
        
        self.fields["account_no"].widget.attrs['readonly '] = True
        # self.fields["account_bank"].widget.attrs['disabled'] = "disabled"


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["account_bank", "account_no", "amount"]
    
    def __init__(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')
        super(WithdrawForm, self).__init__(*args, **kwargs)

        self.fields["account_no"].initial  = account_no
        self.fields["account_bank"].initial  = Account.objects.get(account_no=account_no).bank

        self.fields["account_no"].widget.attrs['readonly '] = True
        # self.fields["account_bank"].widget.attrs['disabled'] = "disabled"


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["account_bank_from", "account_no_from", "account_bank_to", "account_no_to", "amount"]
    
    def __init__(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')
        super(TransferForm, self).__init__(*args, **kwargs)

        if account_no:
            self.fields["account_no_from"].initial  = account_no
            self.fields["account_bank_from"].initial  = Account.objects.get(account_no=account_no).bank
            
            self.fields["account_no_from"].widget.attrs['readonly '] = True
            # self.fields["account_bank_from"].widget.attrs['disabled'] = "disabled"