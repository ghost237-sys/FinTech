from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Budget
from .forms import BudgetForm
from datetime import date

# Create your views here.

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).select_related('category')
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
def budget_add(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
                messages.success(request, 'Budget created successfully.')
                return redirect('budget_list')
            except Exception as e:
                messages.error(request, 'A budget for this category and month already exists.')
    else:
        form = BudgetForm(user=request.user)
    return render(request, 'budgets/budget_form.html', {'form': form})

@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Budget updated successfully.')
                return redirect('budget_list')
            except Exception as e:
                messages.error(request, 'A budget for this category and month already exists.')
    else:
        form = BudgetForm(instance=budget, user=request.user)
    return render(request, 'budgets/budget_form.html', {'form': form, 'budget': budget})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('budget_list')
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})
