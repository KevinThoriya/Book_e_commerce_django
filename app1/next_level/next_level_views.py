from django.shortcuts import render, redirect, HttpResponse
from app1.models import Contact, Register, Book, Cart, Wishlist, Order_details, Transaction
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.templatetags.static import static

import time
import json


# seprate decorator 
def checkLogin(func):
  def wrapper(request):
    if not request.session.get('email'):
        return login_signup(request)
    else:
        return func(request)
  return wrapper








# main controller begins here
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

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = Register.objects.get(email=email, pas=password).first()
            print(user.name)

@checkLogin
def update_profile(request):
    return render(request,'app1/next_level/update_profile.html')

# other ajax requests 
def product_view(request):
    return render(request,'app1/next_level/conponents/product_detail_view.html')
    
def sign_up_form(request):
    return render(request,'app1/next_level/conponents/signup.html')

@csrf_exempt
def book_filter(request):
    time.sleep(2)
    template = loader.get_template('app1/next_level/conponents/product_view.html')
    cate = request.POST.get('categories')
    rendering_div = ''
    product_dic = {}
    if not cate == 'All Categories':
        product_dic.update({'product_image':static('app1/images/next_level/'+cate.lower()+'_demo.png')})
    for i in range(0,10):
        rendering_div += template.render(product_dic,request)
    return HttpResponse(json.dumps({'result': rendering_div}))













