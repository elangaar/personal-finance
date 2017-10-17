from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=40)

    def __str__ (self):
        return self.name

#    def get_absolute_url(self):
#        return reverse('category-list')


class Reminders(models.Model):
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

    def __str__(self):
        return self.name

#    def get_absolute_url(self):
#        return reverse('reminder-list')


class IncomesSources(models.Model):
    name = models.CharField(max_length=40)
    type_of_income = models.CharField(max_length=20)
    permanent = models.BooleanField()

    def __str__(self):
        return self.name + ' - ' + self.type_of_income


class Incomes(models.Model):
    source = models.ForeignKey(IncomesSources)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    income_date = models.DateField(default=date.today)

    def __str__(self):
        return self.source


class Pockets(models.Model):
    name = models.CharField(max_length=40)
    limit = models.DecimalField(max_digits=9, decimal_places=2)
    funds= models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name



class Places(models.Model):
    name= models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    name = models.CharField(max_length=40)
    exp_date = models.DateField(default=date.today)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    pocket = models.ForeignKey(Pockets, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    reminder = models.ForeignKey(Reminders, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
