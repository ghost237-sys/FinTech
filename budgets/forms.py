from django import forms
from .models import Budget
from transactions.models import Category
from datetime import date

class BudgetForm(forms.ModelForm):
    month = forms.CharField(
        widget=forms.DateInput(
            attrs={
                'type': 'month',
                'class': 'form-control',
                'value': date.today().strftime('%Y-%m')
            }
        )
    )

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user, type='expense')
        if self.instance.pk:
            self.initial['month'] = self.instance.month.strftime('%Y-%m')
        
    def clean_month(self):
        month = self.cleaned_data['month']
        try:
            year, month = map(int, month.split('-'))
            return date(year, month, 1)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid month')
