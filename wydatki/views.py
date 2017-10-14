import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from django.db.models import Sum

from wydatki.models import Expenses, Categories, Pockets, Places, Reminders, Incomes, IncomesSources


# Create your views here.


class MainView(TemplateView):
    template_name = "wydatki/index.html"
    

class ExpenseListView(ListView):
    model = Expenses
    
    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        sum_value = Expenses.objects.aggregate(Sum('price'))
        context['sum'] = float(sum_value['price__sum'])
        return context


class ExpenseCreateView(CreateView):
    model = Expenses
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    
    def get_success_url(self):
        return reverse('expense-list')


class CategoryListView(ListView):
    model = Categories

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['amount'] = Categories.objects.count()
        return context


class CategoryCreateView(CreateView):
    model = Categories
    fields = ['name']

    def get_success_url(self):
        return reverse('category-list')


class PocketListView(ListView):
    model = Pockets

    def get_context_data(self, **kwargs):
        context = super(PocketListView, self).get_context_data(**kwargs)
        context['amount'] = Pockets.objects.count()
        return context


class PocketCreateView(CreateView):
    model = Pockets
    fields = ['name', 'limit', 'funds']
    
    def get_success_url(self):
        return reverse('pocket-list')

class PlaceListView(ListView):
    model = Places
    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['amount'] = Places.objects.count()
        return context


class PlaceCreateView(CreateView):
    model = Places
    fields = ['name']

    def get_success_url(self):
        return reverse('place-list')

class ReminderListView(ListView):
    model = Reminders

    def get_context_data(self, **kwargs):
        context = super(ReminderListView, self).get_context_data(**kwargs)
        context['amount'] = Reminders.objects.count()
        return context


class ReminderCreateView(CreateView):
    model = Reminders
    fields = ['remind_date', 'as_before', 'message', 'importance']

    def get_success_url(self):
        return reverse('reminder-list')


class IncomeListView(ListView):
    model = Incomes

    def get_context_data(self, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        sum_value = Incomes.objects.aggregate(Sum('amount'))
        logging.warning(sum_value)
        context['sum'] = float(sum_value['amount__sum'])
        return context


class IncomeCreateView(CreateView):
    model = Incomes
    fields = ['source', 'amount']

    def get_success_url(self):
        return reverse('income-list')


class IncomeSourceListView(ListView):
    model = IncomesSources

    def get_context_data(self, **kwargs):
        context = super(IncomeSourceListView, self).get_context_data(**kwargs)
        context['amount'] = IncomesSources.objects.count()
        return context

class IncomeSourceCreateView(CreateView):
    model = IncomesSources
    fields = ['name', 'type_of_income', 'permanent']

    def get_success_url(self):
        return reverse('income-source-list')

