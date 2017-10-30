from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm


# import logging
# logging.basicConfig(level=logging.DEBUG)



class Category(models.Model):
    name = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_category', 'View category'),
        )


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_reminder', 'View reminder'),
            ('update_reminder', 'Update reminder'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.pk)])


class IncomeSource(models.Model):
    name = models.CharField(max_length=40)
    type_of_income = models.CharField(max_length=20)
    permanent = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_incomesource', 'View income source'),
        )

    def __str__(self):
        return self.name + ' - ' + self.type_of_income

    def get_absolute_url(self):
        return reverse('income-source-detail', args=[str(self.pk)])


class Income(models.Model):
    name = models.CharField(max_length=40)
    source = models.ForeignKey(IncomeSource, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    income_date = models.DateField(default=date.today)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_income', 'View income'),
        )

    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse('income-detail', args=[str(self.pk)])


class Pocket(models.Model):
    name = models.CharField(max_length=40)
    limit = models.DecimalField(max_digits=9, decimal_places=2)
    funds= models.DecimalField(max_digits=9, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_pocket', 'View pocket'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pocket-detail', args=[str(self.pk)])

class Place(models.Model):
    name= models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_place', 'View place'),
        )

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_expense', 'View expense'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('expense-detail', args=[str(self.pk)])



@receiver(post_save, sender=Expense)
def expense_post_save(sender, **kwargs):
    expense, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_expense', user, expense)
    assign_perm('change_expense', user, expense)
    assign_perm('delete_expense', user, expense)

@receiver(post_save, sender=Category)
def category_post_save(sender, **kwargs):
    category, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_category', user, category)
    assign_perm('change_category', user, category)
    assign_perm('delete_category', user, category)

@receiver(post_save, sender=Reminder)
def reminder_post_save(sender, **kwargs):
    reminder, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_reminder', user, reminder)
    assign_perm('change_reminder', user, reminder)
    assign_perm('delete_reminder', user, reminder)

@receiver(post_save, sender=IncomeSource)
def income_source_post_save(sender, **kwargs):
    income_source, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_incomesource', user, income_source)
    assign_perm('change_incomesource', user, income_source)
    assign_perm('delete_incomesource', user, income_source)

@receiver(post_save, sender=Income)
def income_post_save(sender, **kwargs):
    income, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_income', user, income)
    assign_perm('change_income', user, income)
    assign_perm('delete_income', user, income)

@receiver(post_save, sender=Pocket)
def pocket_post_save(sender, **kwargs):
    pocket, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_pocket', user, pocket)
    assign_perm('change_pocket', user, pocket)
    assign_perm('delete_pocket', user, pocket)

@receiver(post_save, sender=Place)
def place_post_save(sender, **kwargs):
    place, user = kwargs['instance'], kwargs['instance'].owner
    assign_perm('view_place', user, place)
    assign_perm('change_place', user, place)
    assign_perm('delete_place', user, place)

