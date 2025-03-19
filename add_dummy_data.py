import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fintech.settings')
django.setup()

from django.contrib.auth import get_user_model
from transactions.models import Category, Transaction
from budgets.models import Budget
from goals.models import Goal

User = get_user_model()

def create_dummy_data(user):
    # Create income categories
    income_categories = [
        Category.objects.create(user=user, name='Salary', type='income'),
        Category.objects.create(user=user, name='Freelance', type='income'),
        Category.objects.create(user=user, name='Investments', type='income')
    ]

    # Create expense categories
    expense_categories = [
        Category.objects.create(user=user, name='Groceries', type='expense'),
        Category.objects.create(user=user, name='Rent', type='expense'),
        Category.objects.create(user=user, name='Utilities', type='expense'),
        Category.objects.create(user=user, name='Entertainment', type='expense'),
        Category.objects.create(user=user, name='Transportation', type='expense')
    ]

    # Create transactions
    current_date = datetime.now()
    for i in range(10):
        # Income transactions
        Transaction.objects.create(
            user=user,
            category=random.choice(income_categories),
            amount=Decimal(random.uniform(1000, 5000)),
            description=f'Income {i+1}',
            date=current_date - timedelta(days=random.randint(0, 90))
        )

        # Expense transactions
        Transaction.objects.create(
            user=user,
            category=random.choice(expense_categories),
            amount=Decimal(random.uniform(50, 1000)),
            description=f'Expense {i+1}',
            date=current_date - timedelta(days=random.randint(0, 90))
        )

    # Create budgets for expense categories
    for category in expense_categories:
        Budget.objects.create(
            user=user,
            category=category,
            amount=Decimal(random.uniform(500, 2000)),
            month=current_date.replace(day=1)
        )

    # Create savings goals
    goals_data = [
        {'name': 'Emergency Fund', 'target': 10000},
        {'name': 'New Car', 'target': 25000},
        {'name': 'Vacation', 'target': 5000}
    ]

    for goal_data in goals_data:
        goal = Goal.objects.create(
            user=user,
            name=goal_data['name'],
            description=f'Saving for {goal_data["name"].lower()}',
            target_amount=Decimal(goal_data['target']),
            current_amount=Decimal(random.uniform(0, goal_data['target'])),
            target_date=current_date + timedelta(days=random.randint(180, 365))
        )
        if goal.current_amount >= goal.target_amount:
            goal.completed = True
            goal.save()

if __name__ == '__main__':
    # Get the first user (you should have at least one user in the system)
    user = User.objects.first()
    if user:
        print(f'Creating dummy data for user: {user.username}')
        create_dummy_data(user)
        print('Dummy data created successfully!')
    else:
        print('No users found in the system. Please create a user first.')
