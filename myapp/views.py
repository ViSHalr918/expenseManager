from typing import Any
from django.shortcuts import render,redirect

from django.views.generic import View

from django.utils import timezone

from myapp.forms import CategoryForm,TransactionForm,TransactionFilterForm,RegistrationForm,LoginForm

from myapp.models import Category,Transactions

from django.db.models import Sum

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from myapp.decorators import signin_required 

from django.utils.decorators import method_decorator


# Create your views here.

@method_decorator(signin_required,name="dispatch")
class CategoryCreateView(View):
    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            messages.error(request,"invalid session...Please login")
            return redirect("login")

        form_instance = CategoryForm(user=request.user)

        qs=Category.objects.filter(owner=request.user)

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            messages.error(request,"invalid session...Please login")
            return redirect("login")

        form_instance=CategoryForm(request.POST,user=request.user,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            # cat_name= form_instance.cleaned_data.get('name')

            # user_obj = request.user
        
            # is_exist = Category.objects.filter(name__iexact=cat_name,owner=user_obj).exists()
        
            # if is_exist:
            #     print("category already exist")
            #     return render(request,"category_add.html",{"form":form_instance,"message":"category already exist"})
            # else:

            form_instance.save()

            # data= form_instance.cleaned_data
            # Category.objects.create(**data)

            return redirect("category-add")
        
        else:
            return render(request,"category_add.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")      
class CategoryUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        category_object = Category.objects.get(id=id)

        form_instance = CategoryForm(instance=category_object)
        return render(request,"category_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id= kwargs.get("pk")

        cat_obj=Category.objects.get(id=id)

        form_instance = CategoryForm(request.POST,instance=cat_obj)

        if form_instance.is_valid():
            form_instance.save()
            return redirect("category-add")
        else:
            return render(request,"category_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")      
class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance = TransactionForm

        cur_month = timezone.now().month

        cur_year = timezone.now().year

        categories = Category.objects.filter(owner=request.user)

        qs = Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)

        return render(request,"transaction_create.html",{"form":form_instance,"transactions":qs,"catogeries":categories})
    
    def post(self,request,*args,**kwargs):

        form_instance = TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transaction-add")
        
        else:
            return render(request,"transaction_create.html",{"form":form_instance})
        





        
@method_decorator(signin_required,name="dispatch")             
class TransactionupdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        trans_obj = Transactions.objects.get(id=id)

        form_instance = TransactionForm(instance=trans_obj)

        return render(request,"transaction_update.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        trans_obj = Transactions.objects.get(id=id)

        form_instance = TransactionForm(request.POST,instance=trans_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
        
        else:

            return render(request,"transaction_update.html",{"form":form_instance})
        



        
@method_decorator(signin_required,name="dispatch")      
class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        Transactions.objects.get(id=id).delete()
        return redirect("transaction-add")
    

@method_decorator(signin_required,name="dispatch")          
class ExpenseSummaryView(View):
    def get(self,request,*args,**kwargs):

        cur_month = timezone.now().month

        cur_year = timezone.now().year

        qs = Transactions.objects.filter(

            created_date__month=cur_month,
            created_date__year=cur_year,
            owner=request.user
        )

        total_expense = qs.values("amount").aggregate(total=Sum("amount")) #{"total":12345}

        payment_summary = qs.values("payment_method").annotate(total=Sum("amount"))
        print(payment_summary)

        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))

        

        data={
            "total":total_expense.get('total'),
            "summary":category_summary,
            "payment":payment_summary
        }
        return render(request,"expense_summary.html",data)
    


    
@method_decorator(signin_required,name="dispatch")      
class TransactionSummaryView(View):
    def get(self,request,*args,**kwargs):

        form_instance = TransactionFilterForm()

        cur_month = timezone.now().month

        cur_year = timezone.now().year

        qs = Transactions.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year
        )

        return render(request,"transaction_summary.html",{"transaction":qs,"form":form_instance})
    





    
class ChartView(View):
    def get(self,request,*args,**kwargs):

        return render(request,"chart.html")



class SignupView(View):
    def get(self,request,*args,**kwargs):
        form_instance =  RegistrationForm()

        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():
            form_instance.save()
            print("Registration Successfull")
            messages.success (request,"Registration Successfull")
            return redirect("sign-in")
        else:
            print("Resistration Not Completed")
            messages.error(request,"Registration failed")
            return render(request,"signin.html",{"form":form_instance})
            

class LoginInView(View):
    def get(self,request,*args,**kwargs):
        form_instance = LoginForm()
        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance =LoginForm(request.POST)

        if form_instance.is_valid():

            data = form_instance.cleaned_data

            user_obj = authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                messages.success(request,"Login successfull")


                return redirect("expense-summary")
        messages.error(request,"Login unsuccessfull,Please check your username and password")       
            
        return render(request,"login.html",{"form":form_instance})
    
    
@method_decorator(signin_required,name="dispatch")              
class SignoutView(View):
    
    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("login")


