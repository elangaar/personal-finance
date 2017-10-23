import logging
logging.basicConfig(level=logging.DEBUG)

from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.db.models import Sum

from wydatki.models import Expense, Category, Pocket, Place, Reminder, Income, IncomeSource




class MainView(TemplateView):
    template_name = "wydatki/index.html"
    

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name='wydatki/my_expense_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user).order_by('exp_date')
    
    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        sum_value = self.get_queryset().aggregate(Sum('price'))
        if sum_value['price__sum'] != None:
            context['sum'] = float(sum_value['price__sum'])
        return context
        


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    
    def get_success_url(self):
        return reverse('my-expense-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ExpenseCreateView, self).form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    template_name_suffix='_update_form'
    
    def get_success_url(self):              # change to expense-detail
        return reverse('expense-list')


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('expense-list')



class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().objects.count()
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']


    def get_success_url(self):
        return reverse('category-list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-source-list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('category-list')


class PocketListView(LoginRequiredMixin, ListView):
    model = Pocket

    def get_queryset(self):
        return Pocket.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(PocketListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class PocketDetailView(LoginRequiredMixin, DetailView):
    model = Pocket


class PocketCreateView(LoginRequiredMixin, CreateView):
    model = Pocket
    fields = ['name', 'limit', 'funds']
    
    def get_success_url(self):
        return reverse('pocket-list')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(PocketCreateView, self).form_valid(form)


class PocketUpdateView(LoginRequiredMixin, UpdateView):
    model = Pocket
    fields = ['name', 'limit', 'funds']
    template_name_suffix='_update_form'
    
    def get_success_url(self):
        return reverse('pocket-list')


class PocketDeleteView(LoginRequiredMixin, DeleteView):
    model = Pocket
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('pocket-list')


class PlaceListView(LoginRequiredMixin, ListView):
    model = Place

    def get_queryset(self):
        return Place.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class PlaceDetailView(LoginRequiredMixin, DetailView):
    model = Place


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    fields = ['name']

    def get_success_url(self):
        return reverse('place-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(PlaceCreateView, self).form_valid(form)


class PlaceUpdateView(LoginRequiredMixin, UpdateView):
    model = Place
    fields = ['name']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('place-list')


class PlaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('place-list')


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder

    def get_queryset(self):
        return Reminder.objects.filter(owner=self.request.user).order_by('-remind_date')

    def get_context_data(self, **kwargs):
        context = super(ReminderListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    fields = ['name', 'remind_date', 'as_before', 'message', 'importance']

    def get_success_url(self):
        return reverse('reminder-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ReminderCreateView, self).form_valid(form)


class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Reminder
    fields = ['name', 'remind_date', 'as_before', 'message', 'importance']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('reminder-list')


class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = Reminder
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('reminder-list')


class IncomeListView(LoginRequiredMixin, ListView):
    model = Income

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user).order_by('source')

    def get_context_data(self, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        sum_value = self.get_queryset().aggregate(Sum('amount'))
        if sum_value['amount__sum'] != None:
            context['sum'] = float(sum_value['amount__sum'])
        return context


class IncomeDetailView(LoginRequiredMixin, DetailView):
    model = Income


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    fields = ['source', 'amount', 'income_date']

    def get_success_url(self):
        return reverse('income-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(IncomeCreateView, self).form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    fields = ['source', 'amount']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-list')


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-list')


class IncomeSourceListView(LoginRequiredMixin, ListView):
    model = IncomeSource

    def get_queryset(self):
        return IncomeSource.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(IncomeSourceListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class IncomeSourceDetailView(LoginRequiredMixin, DetailView):
    model = IncomeSource


class IncomeSourceCreateView(LoginRequiredMixin, CreateView):
    model = IncomeSource
    fields = ['name', 'type_of_income', 'permanent']

    def get_success_url(self):
        return reverse('income-source-list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(IncomeSourceCreateView, self).form_valid(form)


class IncomeSourceUpdateView(LoginRequiredMixin, UpdateView):
    model = IncomeSource
    fields = ['name', 'type_of_income', 'permanent']
    template_name_suffix='_update_form'

    def get_success_url(self):
        return reverse('income-source-list')


class IncomeSourceDeleteView(LoginRequiredMixin, DeleteView):
    model = IncomeSource
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-source-list')
