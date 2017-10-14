from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^list/general/$', views.ExpenseListView.as_view(), name='expense-list'),
    url(r'^list/categories/$', views.CategoryListView.as_view(), name='category-list'),
    url(r'^list/pockets/$', views.PocketListView.as_view(), name='pocket-list'),
    url(r'^list/places/$', views.PlaceListView.as_view(), name='place-list'),
    url(r'^list/reminders/$', views.ReminderListView.as_view(), name='reminder-list'),
    url(r'^list/incomes/$', views.IncomeListView.as_view(), name='income-list'),
    url(r'^list/incomessources/$', views.IncomeSourceListView.as_view(), name='income-source-list'),


    url(r'^add/category/$', views.CategoryCreateView.as_view(), name='category-add'),
    url(r'^add/pocket/$', views.PocketCreateView.as_view(), name='pocket-add'),
    url(r'^add/expense/$', views.ExpenseCreateView.as_view(), name='expense-add'),
    url(r'^add/place/$', views.PlaceCreateView.as_view(), name='place-add'),
    url(r'^add/reminder/$', views.ReminderCreateView.as_view(), name='reminder-add'),
    url(r'^add/income/$', views.IncomeCreateView.as_view(), name='income-add'),
    url(r'^add/incomesource/$', views.IncomeSourceCreateView.as_view(), name='income-source-add'),

    url(r'^expense/(?P<pk>[\d+])/$', views.ExpenseDetailView.as_view(), name='expense-detail'),
    url(r'^category/(?P<pk>[\d+])/$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'^reminder/(?P<pk>[\d+])/$', views.ReminderDetailView.as_view(), name='reminder-detail'),
    url(r'^incomesource/(?P<pk>[\d+])/$', views.IncomeSourceDetailView.as_view(), name='income-source-detail'),
    url(r'^income/(?P<pk>[\d+])/$', views.IncomeDetailView.as_view(), name='income-detail'),
    url(r'^pocket/(?P<pk>[\d+])/$', views.PocketDetailView.as_view(), name='pocket-detail'),
    url(r'^place/(?P<pk>[\d+])/$', views.PlaceDetailView.as_view(), name='place-detail'),

    url(r'^update/expense/$', views.ExpenseUpdateView.as_view(), name='expense-update'),
]
