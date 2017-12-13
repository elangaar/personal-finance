import logging
logging.basicConfig(level=logging.DEBUG)

from django.db.models import Sum
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm

from wydatki.models import Expense, Category, Pocket, Place, Reminder, Income, IncomeSource, Profile
from .forms import UserForm, ExpenseForm, IncomeForm


class MainView(LoginRequiredMixin, TemplateView):
    template_name = "base_main.html"
    

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    paginate_by = 10

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user).order_by('exp_date')
    

    def get_context_data(self, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        sum_value = self.get_queryset().aggregate(Sum('price'))
        if sum_value['price__sum'] != None:
            context['sum'] = float(sum_value['price__sum'])
        return context
        


class ExpenseDetailView(PermissionRequiredMixin, DetailView):
    model = Expense
    permission_required = 'wydatki.view_expense'
    return_403 = True


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    form_class = ExpenseForm
    template_name = 'wydatki/expense_form.html'

    def get_form_kwargs(self):
        kwargs = super(ExpenseCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def get_success_url(self):
        return reverse('expense-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ExpenseCreateView, self).form_valid(form)


class ExpenseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Expense
    fields = ['name', 'exp_date', 'category', 'price', 'pocket', 'place'] # 'reminder'
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_expense'
    return_403 = True
    
    def get_success_url(self):              # change to expense-detail
        return reverse('expense-list')


class ExpenseDeleteView(PermissionRequiredMixin, DeleteView):
    model = Expense
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('expense-list')
    permission_required = 'wydatki.delete_expense'
    return_403 = True


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        category_expenses = {}
        for cat in self.get_queryset():
            cat_exp_sum = Expense.objects.filter(category=cat).aggregate(Sum('price'))
            if cat_exp_sum['price__sum'] != None:
                category_expenses[str(cat)] = cat_exp_sum['price__sum']
        context['category_expenses'] = category_expenses
        return context


class CategoryDetailView(PermissionRequiredMixin, DetailView):
    model = Category
    permission_required = 'wydatki.view_category'
    return_403 = True


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


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category-list')
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_category'
    return_403 = True



class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Category
    template_name='wydatki/confirm_delete.html'
    permission_required = 'wydatki.delete_category'
    return_403 = True

    def get_success_url(self):
        return reverse('category-list')


class PocketListView(LoginRequiredMixin, ListView):
    model = Pocket
    paginate_by = 10

    def get_queryset(self):
        return Pocket.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(PocketListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class PocketDetailView(PermissionRequiredMixin, DetailView):
    model = Pocket
    permission_required = 'wydatki.view_pocket'
    return_403 = True


class PocketCreateView(LoginRequiredMixin, CreateView):
    model = Pocket
    fields = ['name', 'limit', 'funds']
    
    def get_success_url(self):
        return reverse('pocket-list')
    
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            return super(PocketCreateView, self).form_valid(form)
        except IntegrityError as e:
            return HttpResponse('<h1>' + str(e.__cause__) +  '</h1>')

class PocketUpdateView(PermissionRequiredMixin, UpdateView):
    model = Pocket
    fields = ['name', 'limit', 'funds']
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_pocket'
    return_403 = True
    
    def get_success_url(self):
        return reverse('pocket-list')


class PocketDeleteView(PermissionRequiredMixin, DeleteView):
    model = Pocket
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('pocket-list')
    permission_required = 'wydatki.delete_pocket'
    return_403 = True


class PlaceListView(LoginRequiredMixin, ListView):
    model = Place
    paginate_by = 10

    def get_queryset(self):
        return Place.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class PlaceDetailView(PermissionRequiredMixin, DetailView):
    model = Place
    permission_required = 'wydatki.view_place'
    return_403 = True


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


class PlaceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Place
    fields = ['name']
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_place'
    return_403 = True

    def get_success_url(self):
        return reverse('place-list')


class PlaceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Place
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('place-list')
    permission_required = 'wydatki.delete_place'
    return_403 = True


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    paginate_by = 10

    def get_queryset(self):
        return Reminder.objects.filter(owner=self.request.user).order_by('-remind_date')

    def get_context_data(self, **kwargs):
        context = super(ReminderListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class ReminderDetailView(PermissionRequiredMixin, DetailView):
    model = Reminder
    permission_required = 'wydatki.view_reminder'
    return_403 = True


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


class ReminderUpdateView(PermissionRequiredMixin, UpdateView):
    model = Reminder
    fields = ['name', 'remind_date', 'as_before', 'message', 'importance']
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_reminder'
    return_403 = True

    def get_success_url(self):
        return reverse('reminder-list')


class ReminderDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reminder
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('reminder-list')
    permission_required = 'wydatki.delete_reminder'
    return_403 = True


class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    paginate_by = 10

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user).order_by('source')

    def get_context_data(self, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        sum_value = self.get_queryset().aggregate(Sum('amount'))
        if sum_value['amount__sum'] != None:
            context['sum'] = float(sum_value['amount__sum'])
        return context


class IncomeDetailView(PermissionRequiredMixin, DetailView):
    model = Income
    permission_required = 'wydatki.view_income'
    return_403 = True


class IncomeCreateView(LoginRequiredMixin, CreateView):
    form_class = IncomeForm
    template_name = 'wydatki/income_form.html'

    def get_success_url(self):
        return reverse('income-list')

    def get_form_kwargs(self):
        kwargs = super(IncomeCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        logging.debug(kwargs)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(IncomeCreateView, self).form_valid(form)


class IncomeUpdateView(PermissionRequiredMixin, UpdateView):
    model = Income
    fields = ['name', 'source', 'amount', 'income_date']
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_income'
    return_403 = True

    def get_success_url(self):
        return reverse('income-list')


class IncomeDeleteView(PermissionRequiredMixin, DeleteView):
    model = Income
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-list')
    permission_required = 'wydatki.delete_income'
    return_403 = True



class IncomeSourceListView(LoginRequiredMixin, ListView):
    model = IncomeSource
    paginate_by = 10

    def get_queryset(self):
        return IncomeSource.objects.filter(owner=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(IncomeSourceListView, self).get_context_data(**kwargs)
        context['amount'] = self.get_queryset().count()
        return context


class IncomeSourceDetailView(PermissionRequiredMixin, DetailView):
    model = IncomeSource
    permission_required = 'wydatki.view_incomesource'
    return_403 = True


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


class IncomeSourceUpdateView(PermissionRequiredMixin, UpdateView):
    model = IncomeSource
    fields = ['name', 'type_of_income', 'permanent']
    template_name_suffix='_update_form'
    permission_required = 'wydatki.change_incomesource'
    return_403 = True

    def get_success_url(self):
        return reverse('income-source-list')


class IncomeSourceDeleteView(PermissionRequiredMixin, DeleteView):
    model = IncomeSource
    template_name='wydatki/confirm_delete.html'
    success_url = reverse_lazy('income-source-list')
    permission_required = 'wydatki.delete_incomesource'
    return_403 = True


class UserDetailView(DetailView):
    model = User


class UserCreateView(FormView):
    template_name='register.html'
    form_class=UserCreationForm
    success_url='/expenses/'

    def form_valid(self, form):
        form.save()

        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password1', None)
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'wydatki/confirm_delete.html'
    success_url = reverse_lazy('login')


@login_required()
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('picture',))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('index'))
        return render(request, 'user_update_form.html', {
            'noodle': pk,
            'noodle_form': user_form,
            'formset': formset
        })
    else:
        raise PermissionDenied
