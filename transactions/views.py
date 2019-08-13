from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import DepositForm,WithdrawForm,TransferForm
from users.models  import CustomUser, Account
from .models import Withdraw,Deposit,Transfer

def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)

        deposit.account = Account.objects.get(account_no=deposit.account_no)

        deposit.user_name = deposit.account.user.full_name
        deposit.save()

        deposit.account.balance += deposit.amount
        deposit.account.save()
        
        messages.success(request, 'You Have Deposited .'.format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "DW/dw.htm", context)

def withdraw_view(request):
    form = WithdrawForm(request.POST or None)

    if form.is_valid():
        withdraw= form.save(commit=False)

        withdraw.account = Account.objects.get(account_no=withdraw.account_no)

        withdraw.user_name = withdraw.account.user.full_name
        withdraw.save()
        
        withdraw.account.balance-=withdraw.amount
        withdraw.account.save()

        messages.success(request, 'You Have Withdrawn .'.format(withdraw.amount))
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "DW/dw.htm", context)

def transfer_view(request):
    form = TransferForm(request.POST or None)

    if form.is_valid():
        transfer = form.save(commit=False)

        # 보내는 계좌의 잔고를 뺀다
        transfer.account = Account.objects.get(account_no=transfer.account_no_from)
        transfer.user_name = CustomUser.objects.get(email=request.user).full_name
        transfer.account.balance -= transfer.amount

        # 받는 계좌의 잔고를 더한다
        receiver_obj = Account.objects.get(account_no=transfer.account_no_to)
        receiver_obj.balance += transfer.amount

        # 추가 정보 저장한다
        transfer.receiver_id = receiver_obj.user.id
        transfer.receiver_name = receiver_obj.user.full_name

        receiver_obj.save()
        transfer.save()
        

        messages.success(request, 'You Have Sent Money .'.format(transfer.amount))
        return redirect("home")

    context = {
        "title": "Transfer",
        "form": form
    }
    return render(request, "DW/dw.htm", context)


def transcations_detail(request):
    user = request.user
    dep_obj  = Deposit.objects.filter(user=user)
    with_obj = Withdraw.objects.filter(user=user)
    Td_obj   = Transfer.objects.filter(user=user)
    Tc_obj   = Transfer.objects.filter(receiver_id=user.id)

    context={
        'dep_obj':dep_obj,
        'with_obj':with_obj,
        'Td_obj':Td_obj,
        'Tc_obj':Tc_obj,
    }

    return render(request,'Trans/trans.htm', context)


def transcations_summary(request):
    user = request.user
    dep_obj  = Deposit.objects.filter(user=user)
    with_obj = Withdraw.objects.filter(user=user)
    Td_obj   = Transfer.objects.filter(user=user)
    Tc_obj   = Transfer.objects.filter(receiver_id=user.id)

    context={
        'dep_obj':dep_obj,
        'with_obj':with_obj,
        'Td_obj':Td_obj,
        'Tc_obj':Tc_obj,
    }

    return render(request,'Trans/mini.htm', context)
