"""
URL configuration for expensemanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path("category/add/",views.CategoryCreateView.as_view(),name="category-add"),

    path("category/<int:pk>/edit/",views.CategoryUpdateView.as_view(),name="cat-edit"),

    path("transaction/add/",views.TransactionCreateView.as_view(),name="transaction-add"),

    path('transaction/<int:pk>/edit',views.TransactionupdateView.as_view(),name="trans-edit"),

    path("transaction/<int:pk>/delete",views.TransactionDeleteView.as_view(),name="trans-delete"),
    
    path('expense/summary/',views.ExpenseSummaryView.as_view(),name='expense-summary'),

    path("transaction/summary/",views.TransactionSummaryView.as_view(),name="transaction-summary"),

    path("chart/",views.ChartView.as_view(),name="chart"),

    path("registration/",views.SignupView.as_view(),name="sign-in"),

    path("",views.LoginInView.as_view(),name="login"),

    path("logout/",views.SignoutView.as_view(),name="logout")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
