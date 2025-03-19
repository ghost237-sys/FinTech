from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from transactions.models import Transaction
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict

# Create your views here.

@login_required
def reports(request):
    return render(request, 'reports/reports.html')

@login_required
def income_expense_chart(request):
    income = Transaction.objects.filter(
        user=request.user,
        category__type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense = Transaction.objects.filter(
        user=request.user,
        category__type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    return JsonResponse({
        'income': float(income),
        'expense': float(expense)
    })

@login_required
def category_distribution_chart(request):
    expenses = Transaction.objects.filter(
        user=request.user,
        category__type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    categories = {
        expense['category__name']: float(expense['total'])
        for expense in expenses
    }

    return JsonResponse({
        'categories': categories
    })

@login_required
def monthly_trends_chart(request):
    # Get data for the last 6 months
    end_date = timezone.now().date().replace(day=1)
    start_date = (end_date - timedelta(days=180)).replace(day=1)
    
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lt=end_date + timedelta(days=32)
    ).values('date', 'amount', 'category__type')

    trends = defaultdict(lambda: {'income': 0, 'expense': 0})
    
    for transaction in transactions:
        month = transaction['date'].strftime('%Y-%m')
        amount = float(transaction['amount'])
        if transaction['category__type'] == 'income':
            trends[month]['income'] += amount
        else:
            trends[month]['expense'] += amount

    # Sort by month
    sorted_trends = dict(sorted(trends.items()))

    return JsonResponse({
        'trends': sorted_trends
    })
