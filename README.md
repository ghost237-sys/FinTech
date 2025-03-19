# Fintech - Personal Finance Management System

A comprehensive financial management application built with Django that helps users track their finances, manage budgets, and achieve savings goals.

## Features

- User Authentication
  - Sign up, log in, and log out functionality
  - Secure password management

- Dashboard
  - Overview of financial status
  - Quick summary of income, expenses, and savings

- Transaction Management
  - Add, edit, and delete transactions
  - Categorize transactions
  - Transaction history

- Budgeting
  - Create and manage category-wise budgets
  - Track budget progress
  - Budget alerts

- Savings Goals
  - Set financial goals
  - Track progress towards goals
  - Goal completion notifications

- Reports & Analytics
  - Visual representation of financial data
  - Monthly/yearly comparisons
  - Category-wise analysis

- Dark/Light Mode
  - Toggle between themes
  - Persistent theme preference

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Tech Stack

- Django 5.0.0
- Bootstrap 5
- Chart.js
- SQLite (default database)
# FinTech
