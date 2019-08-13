from django.shortcuts import render, redirect

# Create your views here.

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.generic.base import TemplateView

from .models import CustomUser, Account 
from .forms import CustomUserCreationForm,PasswordChangeForm, AccountForm

from transactions.models import Withdraw,Deposit,Transfer


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.htm', {
        'form': form
    })
    

class Home(TemplateView):

    def get(self, request, *args, **kwargs):
        context={}
        
        is_authenticated = request.user.is_authenticated
        

        if is_authenticated == True:
            user = CustomUser.objects.get(email=request.user)

            account_obj = Account.objects.filter(user=user.id)

            dep_obj  = Deposit.objects.filter(user_name=user.full_name)
            with_obj = Withdraw.objects.filter(user_name=user.full_name)
            Td_obj   = Transfer.objects.filter(user_name=user.full_name)
            Tc_obj   = Transfer.objects.filter(receiver_name=user.full_name)

            context={
                'account_obj':account_obj,
                'dep_obj':dep_obj,
                'with_obj':with_obj,
                'Td_obj':Td_obj,
                'Tc_obj':Tc_obj,
            }
        
        return render(request,'home.htm', context)


def account_view(request):
    form = AccountForm(request.POST or None)

    if form.is_valid():
        
        account = form.save(commit=False)
        account.user = CustomUser.objects.get(email=request.user)


        # 기존에 주 계좌로 설정된 계좌가 존재한다면
        if (account.user.main_account_no != '') and (account.is_main_account == True):

            # 기존의 주 계좌 설정을 False로 변경하고
            prev_main_account = Account.objects.get(account_no = account.user.main_account_no)
            prev_main_account.is_main_account = False
            prev_main_account.save()

        # 해당 사용자의 주 계좌 번호를 변경
        account.user.main_account_no = account.account_no
        account.user.save()
        account.save()
        
        messages.success(request, 'You Created Account .'.format(account.account_no))

        return redirect("home")

    context = {
        "title": "Account",
        "form": form
    }
    return render(request, "Account/account.htm", context)