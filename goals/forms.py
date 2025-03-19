from django import forms
from .models import Goal
from datetime import date

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'target_amount', 'target_date']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
