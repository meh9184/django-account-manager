from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ValidationError

from .forms import DepositForm,WithdrawForm,TransferForm
from .models import Withdraw,Deposit,Transfer

from users.models  import CustomUser, Account

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
        withdraw = form.save(commit=False)

        withdraw.account = Account.objects.get(account_no=withdraw.account_no)

        # 1회 한도 초과되는지 검토
        if withdraw.account.limit_once < withdraw.amount:
            raise ValidationError("Can only withdraw up to . at a time".format(withdraw.account.limit_once))
        # 1일 한도 초과되는지 검토
        elif (withdraw.account.limit_daily - withdraw.amount) < 0:
            raise ValidationError("Expire daily withdraw limit")
        else:
            # 1일 제한량에서 amount 만큼 감소한 후 출금 진행
            withdraw.account.limit_daily -= withdraw.amount
            
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
        transfer.account = Account.objects.get(account_no=transfer.account_no_from)

        commission = 0

        # 보내는 계좌와 받는 계좌의 은행이 다른지 확인 (같다면 수수료 면제)
        if transfer.account.bank != Account.objects.get(account_no=transfer.account_no_to).bank:
        
            # 보내는 계좌의 하루 이체 건수 확인
            if transfer.account.daily_transfer_number <= 0:
                # 초과했다면 수수료 500원 부과
                commission += 500
            else:
                # 초과하지 않았다면 이체 건수 하나 감소
                transfer.account.daily_transfer_number -= 1

        # 보내는 계좌의 잔고를 차감
        transfer.user_name = CustomUser.objects.get(email=request.user).full_name
        transfer.account.balance -= (transfer.amount + commission)
        transfer.account.save()

        # 받는 계좌의 잔고를 누산
        receiver_obj = Account.objects.get(account_no=transfer.account_no_to)
        receiver_obj.balance += (transfer.amount + commission)

        # 추가 정보 저장
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
