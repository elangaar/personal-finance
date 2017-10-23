from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.pk)])


class Reminder(models.Model):
    PRIORITIES= (
        ('BW', 'Bardzo ważny'),
        ('W', 'Ważny'),
        ('M', 'Mało ważny'),
    )
    name = models.CharField(max_length=30)
    remind_date = models.DateField()
    as_before= models.DateField()
    message= models.CharField(max_length=100)
    importance= models.CharField(max_length=2, choices=PRIORITIES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.pk)])


class IncomeSource(models.Model):
    name = models.CharField(max_length=40)
    type_of_income = models.CharField(max_length=20)
    permanent = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name + ' - ' + self.type_of_income

    def get_absolute_url(self):
        return reverse('income-source-detail', args=[str(self.pk)])


class Income(models.Model):
    source = models.ForeignKey(IncomeSource)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    income_date = models.DateField(default=date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.source

    
    def get_absolute_url(self):
        return reverse('income-detail', args=[str(self.pk)])


class Pocket(models.Model):
    name = models.CharField(max_length=40)
    limit = models.DecimalField(max_digits=9, decimal_places=2)
    funds= models.DecimalField(max_digits=9, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pocket-detail', args=[str(self.pk)])

class Place(models.Model):
    name= models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('place-detail', args=[str(self.pk)])


class Expense(models.Model):
    name = models.CharField(max_length=40)
    exp_date = models.DateField(default=date.today)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    pocket = models.ForeignKey(Pocket, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('expense-detail', args=[str(self.pk)])
