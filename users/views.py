from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum
from transactions.models import Transaction
from goals.models import Goal
from datetime import datetime
from .forms import UserRegisterForm, UserUpdateForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get recent transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
    
    # Calculate totals
    income = Transaction.objects.filter(
        user=request.user,
        category__type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    expenses = Transaction.objects.filter(
        user=request.user,
        category__type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = income - expenses

    # Get active goals
    goals = Goal.objects.filter(user=request.user, completed=False).order_by('target_date')

    context = {
        'transactions': transactions,
        'goals': goals,
        'total_income': income,
        'total_expenses': expenses,
        'balance': balance
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'users/logout.html')
