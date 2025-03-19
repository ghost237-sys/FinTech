from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from .forms import GoalForm
from decimal import Decimal

# Create your views here.

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/goal_list.html', {'goals': goals})

@login_required
def goal_add(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully.')
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form})

@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully.')
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form, 'goal': goal})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully.')
        return redirect('goal_list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})

@login_required
def goal_update_progress(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', 0))
            if amount <= 0:
                raise ValueError('Amount must be positive')
            goal.update_progress(amount)
            messages.success(request, f'Added {amount} to your goal progress.')
            if goal.completed:
                messages.success(request, 'Congratulations! You have reached your goal!')
            return redirect('goal_list')
        except (ValueError, TypeError) as e:
            messages.error(request, str(e) or 'Please enter a valid amount.')
    return render(request, 'goals/goal_update_progress.html', {'goal': goal})
