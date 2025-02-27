from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import Account
from .forms import AccountCreationForm, AccountUpdateForm, LoginForm, ChangePasswordForm

import traceback
import json

# Create your views here.
@login_required(login_url="/accounts/login/")
def accounts(request):
    account = Account.objects.filter(is_active=True).order_by('-id')
    
    per_page = 10
    paginator = Paginator(account, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"errors : {exc}\ntrace : {tb}")
        return render(request, 'accounts.html', {'exception': exc})
    return render(request, 'accounts.html', {'data':data,'paginator':paginator})

@login_required(login_url="/accounts/login/")
def insert_account(request):
    form = AccountCreationForm(request.POST or None)
    form_type = 'insert'
    if request.method == 'POST':
        if form.is_valid():
            if not form.cleaned_data.get('password'):
                form.add_error('password', 'Password is required')
            else:
                form.save()
                return redirect('/accounts')
    
    context = {
        'form':form,
        'form_type':form_type
    }
    return render(request, 'account_form.html', context)

@login_required(login_url="/accounts/login/")
def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AccountUpdateForm(request.POST or None, instance=account)
    form_type = 'update'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/accounts')
    
    context = {
        'form':form,
        'form_type':form_type
    }
    return render(request, 'account_form.html', context)

@login_required(login_url="/accounts/login/")
def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = ChangePasswordForm(account, request.POST or None)
    
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, account)
        return redirect('/accounts')
    
    context = {
        'form':form
    }
    return render(request, 'change_password.html', context)

@login_required(login_url="/accounts/login/")
def delete_account(request, pk):
    Account.deactivate(pk)
    return redirect('/accounts')

def deauth(request):
    logout(request)
    return redirect('/accounts/login/')

def auth(request):
    form = LoginForm(request, data=request.POST or None)
    context = {
        'form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                # check role and redirect here
                return redirect('/dashboard')
            else:
                context.update({'message':'Invalid username or password'})
                return render(request, 'login.html',context)
        else:
            context.update({'message':'Invalid username or password'})
            return render(request, 'login.html',context)
    return render(request, 'login.html',context)