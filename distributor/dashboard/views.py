from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib import messages
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncWeek, TruncDay
from django.http import JsonResponse
from django.utils import timezone
import datetime
from .forms import DistributorLoginForm
from ajax_datatable.views import AjaxDatatableView
from rest_framework import viewsets
from .serializers import TransactionSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = DistributorLoginForm(request, data=request.POST)
        if form.is_valid():
            distributor_id = form.cleaned_data.get('username')
            distributor_name = form.cleaned_data.get('password')
            
            # start_date = form.cleaned_data['start_date']
            # end_date = form.cleaned_data['end_date']
            
            user = authenticate(request, username=distributor_id, password=distributor_name)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('dashboard/')  # Redirect to your dashboard
            else:
                # Show an error message
                form.add_error(None, "Invalid distributor ID or name.")
                return HttpResponseRedirect('login')
    else:
        form = DistributorLoginForm()
    return render(request, 'dashboard/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    distributor = request.user
    distributor_id = distributor.id

    # Date range filter (handle form submission)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = timezone.now() - datetime.timedelta(days=30)  # Default: last 30 days
    end_date = timezone.now()
    # if start_date_str and end_date_str:
    #     start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    #     end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Get transactions for the distributor within the date range
    transactions = Transaction.objects.filter(
        distributor=distributor_id,
        date__range=[start_date, end_date]
    )

    # --- Daily Earnings ---
    daily_earnings = (
        transactions.annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product') * F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
        .order_by('day')
    )

    # --- Weekly Earnings ---
    weekly_earnings = (
        transactions.annotate(week=TruncWeek('date'))
        .values('week')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product__price') *
                F('product__category') + F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
        .order_by('week')
    )

    # --- Product Category Earnings ---
    category_earnings = (
        transactions.values('product__category')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product__price') *
                F('product__category')+F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
    )

    context = {
        'daily_earnings': list(daily_earnings),
        'weekly_earnings': list(weekly_earnings),
        'category_earnings': list(category_earnings),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def transaction(request):
    # Fetch the logged-in user's profile
    user_profile = request.user  # Assuming each user has a corresponding profile
    distributor_id = user_profile.id

    # Filter transactions based on the user's distributor credentials
    transactions = Transaction.objects.filter(
        distributor=distributor_id, 
    )
    
    context ={
        'transactions':list(transactions),
    }
    return render(request, 'dashboard/transaction_list.html',context)

def daily_earnings_chart_data(request):
    distributor = request.user

    # Date range filter (handle form submission)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = timezone.now() - datetime.timedelta(days=30)  # Default: last 30 days
    end_date = timezone.now()
    if start_date_str and end_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Get transactions for the distributor within the date range
    transactions = Transaction.objects.filter(
        distributor=distributor,
        date__range=[start_date, end_date]
    )

    # --- Daily Earnings ---
    daily_earnings = (
        transactions.annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product__price') *
                F('product__category')+F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
        .order_by('day')
    )

    # Prepare data for Chart.js
    labels = [earning['day'].strftime('%Y-%m-%d') for earning in daily_earnings]
    data = [earning['total_earnings'] for earning in daily_earnings]

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Daily Earnings',
            'data': data,
            # ... other chart.js options
        }]
    }
    return JsonResponse(chart_data)

def weekly_earnings_chart_data(request):
    distributor = request.user

    # Date range filter (handle form submission)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = timezone.now() - datetime.timedelta(days=30)  # Default: last 30 days
    end_date = timezone.now()
    if start_date_str and end_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Get transactions for the distributor within the date range
    transactions = Transaction.objects.filter(
        distributor=distributor,
        date__range=[start_date, end_date]
    )

    # --- Weekly Earnings ---
    weekly_earnings = (
        transactions.annotate(week=TruncWeek('date'))
        .values('week')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product__price') *
                F('product__category') + F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
        .order_by('week')
    )

    # Prepare data for Chart.js
    labels = [earning['week'].strftime('%Y-%m-%d') for earning in weekly_earnings]
    data = [earning['total_earnings'] for earning in weekly_earnings]

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Weekly Earnings',
            'data': data,
            # ... other chart.js options
        }]
    }
    return JsonResponse(chart_data)

def category_earnings_chart_data(request):
    distributor = request.user

    # Date range filter (handle form submission)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = timezone.now() - datetime.timedelta(days=30)  # Default: last 30 days
    end_date = timezone.now()
    if start_date_str and end_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Get transactions for the distributor within the date range
    transactions = Transaction.objects.filter(
        distributor=distributor,
        date__range=[start_date, end_date]
    )

    category_earnings = (
        transactions.values('product__category')
        .annotate(total_earnings=Sum(
            ExpressionWrapper(
                F('product__price') *
                F('product__category')+F('commission') / 100.00,
                output_field=DecimalField()
            )
        ))
    )

    # Prepare data for Chart.js
    labels = [earning['product__category'] for earning in category_earnings]
    data = [earning['total_earnings'] for earning in category_earnings]

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Category Earnings',
            'data': data,
            # ... other chart.js options
        }]
    }
    return JsonResponse(chart_data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
def transaction_list(request):
    return render(request, 'dashboard/dashboard.html')

class TransactionDataTableView(AjaxDatatableView):
    model = Transaction
    title = 'Transactions Data Tables'
    column_defs = [
        'Transaction_id',
        'date',
        'Customer',
        'Product',
        'Merchant',
        'Commission'
    ]
