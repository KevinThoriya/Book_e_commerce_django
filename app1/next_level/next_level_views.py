from django.shortcuts import render, redirect, HttpResponse
from app1.models import Contact, Register, Book, Cart, Wishlist, Order_details, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
import json

def index(request):
    return render(request,'app1/next_level/index.html')

def product_detail(request):
    return render(request,'app1/next_level/product_detail_page.html')

def about_us(request):
    return render(request,'app1/next_level/about.html')

def book_list(request):
    # Sorting, filtering of book done here based on passing pera 
    return render(request,'app1/next_level/book_list.html')

def services(request):
    return render(request,'app1/next_level/services.html')

def login_signup(request):
    return render(request,'app1/next_level/login_signup.html')



# other ajax requests 
def product_view(request):
    return render(request,'app1/next_level/conponents/product_detail_view.html')
    
def sign_up_form(request):
    return render(request,'app1/next_level/conponents/signup.html')

@csrf_exempt
def book_filter(request):
    template = loader.get_template('app1/next_level/conponents/product_view.html')
    product_dic = {}
    rendering_div = template.render(product_dic,request)
    return HttpResponse(json.dumps({'result': rendering_div}))