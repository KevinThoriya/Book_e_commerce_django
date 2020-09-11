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







# get common values 
def get_common_values(request):
    values = {}
    if request.session.get('email'):
        user = Register.objects.filter(email=request.session.get('email')).first()
        values.update({'user':user})
    return  values




# main controller begins here
def index(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/index.html',context)

def product_detail(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/product_detail_page.html',context)

def about_us(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/about.html',context)

def book_list(request):
    context = get_common_values(request)
    # Sorting, filtering of book done here based on passing pera 
    return render(request,'app1/next_level/book_list.html',context)

def services(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/services.html',context)

def login_signup(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/login_signup.html',context)

def login(request):
    context = get_common_values(request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            user = Register.objects.get(email=email, pas=password).first()
            print(user.name)

@checkLogin
def update_profile(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/update_profile.html',context)

@checkLogin
def manage_product_order(request):
    context = get_common_values(request)
    context.update({ 'books' : [1,2,3,4,5,6,7,8,9] })
    return render(request,'app1/next_level/seller_book_list.html',context)


@checkLogin
def manage_edit_book(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/seller_book_edit.html',context)

@checkLogin
def my_order(request):
    context = get_common_values(request)
    return  render(request,'app1/next_level/my_order.html',context)


# other ajax requests 
def product_view(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/conponents/product_detail_view.html',context)
    
def sign_up_form(request):
    context = get_common_values(request)
    return render(request,'app1/next_level/conponents/signup.html',context)

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













