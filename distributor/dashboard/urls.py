from django.urls import path,include
from . import views
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('daily_earnings_chart_data/', views.daily_earnings_chart_data, name='daily_earnings_chart_data'),
    path('weekly_earnings_chart_data/', views.weekly_earnings_chart_data, name='weekly_earnings_chart_data'),
    path('category_earnings_chart_data/', views.category_earnings_chart_data, name='category_earnings_chart_data'),
    path('transactions/', views.transaction, name='transaction_list'),
    path('transactions/json/', views.TransactionDataTableView.as_view(), name='transaction_list_json'),
    path('api/', include(router.urls)),
    
    # Login and logout routes
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]