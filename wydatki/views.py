import logging
logging.basicConfig(level=logging.DEBUG)

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

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
        if sum_value['price__sum'] != None:
            context['sum'] = float(sum_value['price__sum'])
        return context


class ExpenseDetailView(DetailView):
    model = Expenses


class ExpenseCreateView(CreateView):
    model = Expenses
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    
    def get_success_url(self):
        return reverse('expense-list')


class ExpenseUpdateView(UpdateView):
    model = Expenses
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    template_name_suffix='_update_form'
    
    def get_success_url(self):              # change to expense-detail
        return reverse('expense-list')


class ExpenseDeleteView(DeleteView):
    model = Expenses
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('expense-list')



class CategoryListView(ListView):
    model = Categories

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['amount'] = Categories.objects.count()
        return context


class CategoryDetailView(DetailView):
    model = Categories


class CategoryCreateView(CreateView):
    model = Categories
    fields = ['name']

    def get_success_url(self):
        return reverse('category-list')


class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ['name']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-source-list')


class CategoryDeleteView(DeleteView):
    model = Categories
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('category-list')


class PocketListView(ListView):
    model = Pockets

    def get_context_data(self, **kwargs):
        context = super(PocketListView, self).get_context_data(**kwargs)
        context['amount'] = Pockets.objects.count()
        return context


class PocketDetailView(DetailView):
    model = Pockets


class PocketCreateView(CreateView):
    model = Pockets
    fields = ['name', 'limit', 'funds']
    
    def get_success_url(self):
        return reverse('pocket-list')


class PocketUpdateView(UpdateView):
    model = Pockets
    fields = ['name', 'limit', 'funds']
    template_name_suffix='_update_form'
    
    def get_success_url(self):
        return reverse('pocket-list')


class PocketDeleteView(DeleteView):
    model = Pockets
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('pocket-list')


class PlaceListView(ListView):
    model = Places
    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['amount'] = Places.objects.count()
        return context


class PlaceDetailView(DetailView):
    model = Places


class PlaceCreateView(CreateView):
    model = Places
    fields = ['name']

    def get_success_url(self):
        return reverse('place-list')


class PlaceUpdateView(UpdateView):
    model = Places
    fields = ['name']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('place-list')


class PlaceDeleteView(DeleteView):
    model = Places
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('place-list')


class ReminderListView(ListView):
    model = Reminders

    def get_context_data(self, **kwargs):
        context = super(ReminderListView, self).get_context_data(**kwargs)
        context['amount'] = Reminders.objects.count()
        return context


class ReminderDetailView(DetailView):
    model = Reminders


class ReminderCreateView(CreateView):
    model = Reminders
    fields = ['name', 'remind_date', 'as_before', 'message', 'importance']

    def get_success_url(self):
        return reverse('reminder-list')


class ReminderUpdateView(UpdateView):
    model = Reminders
    fields = ['name', 'remind_date', 'as_before', 'message', 'importance']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('reminder-list')


class ReminderDeleteView(DeleteView):
    model = Reminders
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('reminder-list')


class IncomeListView(ListView):
    model = Incomes

    def get_context_data(self, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        sum_value = Incomes.objects.aggregate(Sum('amount'))
        if sum_value['amount__sum'] != None:
            context['sum'] = float(sum_value['amount__sum'])
        return context


class IncomeDetailView(DetailView):
    model = Incomes


class IncomeCreateView(CreateView):
    model = Incomes
    fields = ['source', 'amount', 'income_date']

    def get_success_url(self):
        return reverse('income-list')


class IncomeUpdateView(UpdateView):
    model = Incomes
    fields = ['source', 'amount']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-list')


class IncomeDeleteView(DeleteView):
    model = Incomes
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-list')


class IncomeSourceListView(ListView):
    model = IncomesSources

    def get_context_data(self, **kwargs):
        context = super(IncomeSourceListView, self).get_context_data(**kwargs)
        context['amount'] = IncomesSources.objects.count()
        return context


class IncomeSourceDetailView(DetailView):
    model = IncomesSources


class IncomeSourceCreateView(CreateView):
    model = IncomesSources
    fields = ['name', 'type_of_income', 'permanent']

    def get_success_url(self):
        return reverse('income-source-list')


class IncomeSourceUpdateView(UpdateView):
    model = IncomesSources
    fields = ['name', 'type_of_income', 'permanent']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-source-list')


class IncomeSourceDeleteView(DeleteView):
    model = IncomesSources
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-source-list')
