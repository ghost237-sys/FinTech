from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Category
from .forms import TransactionForm

# Create your views here.

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('category').order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transactions/transaction_form.html', {'form': form})

@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'transactions/transaction_form.html', {'form': form, 'transaction': transaction})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def category_list(request):
    return render(request, 'transactions/category_list.html')

@login_required
def category_add(request):
    return render(request, 'transactions/category_form.html')

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    return render(request, 'transactions/category_form.html', {'category': category})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'transactions/category_confirm_delete.html', {'category': category})
