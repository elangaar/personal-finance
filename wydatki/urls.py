from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^list/expenses/$', views.ExpenseListView.as_view(), name='expense-list'),
    url(r'^list/expenses/user/', views.ExpenseUserListView.as_view(),
    name='my-expense-list' ),
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

    url(r'^expense/(?P<pk>[\d]+)/$', views.ExpenseDetailView.as_view(), name='expense-detail'),
    url(r'^category/(?P<pk>[\d]+)/$', views.CategoryDetailView.as_view(), name='category-detail'),
    url(r'^reminder/(?P<pk>[\d]+)/$', views.ReminderDetailView.as_view(), name='reminder-detail'),
    url(r'^incomesource/(?P<pk>[\d]+)/$', views.IncomeSourceDetailView.as_view(), name='income-source-detail'),
    url(r'^income/(?P<pk>[\d]+)/$', views.IncomeDetailView.as_view(), name='income-detail'),
    url(r'^pocket/(?P<pk>[\d]+)/$', views.PocketDetailView.as_view(), name='pocket-detail'),
    url(r'^place/(?P<pk>[\d]+)/$', views.PlaceDetailView.as_view(), name='place-detail'),

    url(r'^update/expense/(?P<pk>[\d]+)/$', views.ExpenseUpdateView.as_view(), name='expense-update'),
    url(r'^update/category/(?P<pk>[\d]+)/$', views.CategoryUpdateView.as_view(), name='category-update'),
    url(r'^update/reminder/(?P<pk>[\d]+)/$', views.ReminderUpdateView.as_view(), name='reminder-update'),
    url(r'^update/incomesource/(?P<pk>[\d]+)/$', views.IncomeSourceUpdateView.as_view(), name='income-source-update'),
    url(r'^update/income/(?P<pk>[\d]+)/$', views.IncomeUpdateView.as_view(), name='income-update'),
    url(r'^update/pocket/(?P<pk>[\d]+)/$', views.PocketUpdateView.as_view(), name='pocket-update'),
    url(r'^update/place/(?P<pk>[\d]+)/$', views.PlaceUpdateView.as_view(), name='place-update'),
    
    url(r'^delete/expense/(?P<pk>[\d]+)/$', views.ExpenseDeleteView.as_view(), name='expense-delete'),
    url(r'^delete/category/(?P<pk>[\d]+)/$', views.CategoryDeleteView.as_view(), name='category-delete'),
    url(r'^delete/reminder/(?P<pk>[\d]+)/$', views.ReminderDeleteView.as_view(), name='reminder-delete'),
    url(r'^delete/incomesource/(?P<pk>[\d]+)/$', views.IncomeDeleteView.as_view(), name='income-source-delete'),
    url(r'^delete/income/(?P<pk>[\d]+)/$', views.IncomeDeleteView.as_view(), name='income-delete'),
    url(r'^delete/pocket/(?P<pk>[\d]+)/$', views.PocketDeleteView.as_view(), name='pocket-delete'),
    url(r'^delete/place/(?P<pk>[\d]+)/$', views.PlaceDeleteView.as_view(), name='place-delete'),
]
