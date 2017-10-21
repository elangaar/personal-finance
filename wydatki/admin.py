from django.contrib import admin
from .models import Category, Reminder, IncomeSource, Income, Pocket, Place, Expense

admin.site.register(Category)
admin.site.register(Reminder)
admin.site.register(IncomeSource)
admin.site.register(Income)
admin.site.register(Pocket)
admin.site.register(Place)
admin.site.register(Expense)
