from django import forms
from django.contrib.auth.models import User
from wydatki.models import Expense, Category, Pocket, Place, Income, IncomeSource

import logging
logging.basicConfig(level=logging.DEBUG)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place']  # 'reminder'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=user)
        self.fields['pocket'].queryset = Pocket.objects.filter(owner=user)
        self.fields['place'].queryset = Place.objects.filter(owner=user)

    
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'source', 'amount', 'income_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id')
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset=IncomeSource.objects.filter(owner=user)

