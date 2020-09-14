from django.shortcuts import render, redirect, HttpResponse
from app1.models import Contact, Register, Book, Cart, Wishlist, Order_details, Transaction, Offer_banner
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
    context.update({
        'offers' : Offer_banner.running_offers()
    })
    print(context)
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

    context.update({
        'image_url' :  static('app1/images/next_level/react_demo.png'),
        'book_short_name' : 'Book Short Name',
        'book_name' : 'Pro Scala Seed React with Play Framework By Kevin Thoriya',
        'book_headline' : 'With full of Great Content about Play Framework to make you Hero from Zero in Scala as Well as React',
        'long_disc' : """Use play framework to develop the application backend/services and frontend using React Create App, all in a totally integrated workflow and single unified console. This approach will deliver perfect development experience without CORS hassle. Fork or clone the seed project of your language preference and get started:
                        Are you building a web application with React? React is super cool! We all know that. But are you looking for a good backend framework to pair with it? No clue on how to get started without going through the pain of setting up things from scratch. Doesn’t matter whether you are building a production ready application or a proof of concept project, You are at the correct place, let’s dive into detail.
                        """,
        'price' : '13.00',
        'book_type' : 'Coding, Scala Programing, React, Seed, Play Framework',
        'short_headline' : 'some product text comes here about book we can say',
    })
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
        product_dic.update({'image_url':static('app1/images/next_level/'+cate.lower()+'_demo.png')})
    for i in range(0,10):
        rendering_div += template.render(product_dic,request)
    return HttpResponse(json.dumps({'result': rendering_div}))


@csrf_exempt
def preview_book(request):
    template = loader.get_template('app1/next_level/conponents/' + ('product_detail_view.html' if request.POST.get('preview_for') == 'full_page' else 'product_view.html'))
    context = get_common_values(request)
    context.update({
        'image_url' : request.POST.get('image_url'),
        'book_short_name' : request.POST.get('book_short_name'),
        'book_name' : request.POST.get('book_name'),
        'book_headline' : request.POST.get('book_headline'),
        'long_disc' : request.POST.get('long_disc'),
        'price' : request.POST.get('price'),
        'book_type' : request.POST.get('book_type'),
        'short_headline' : request.POST.get('short_headline'),
    })
    rendering_div = ''
    if request.POST.get('preview_for') == 'full_page':
        rendering_div = template.render(context,request )
    else : 
        rendering_div = '<div class="row wid-hei-90">'
        for i in range(0,4):
            rendering_div += template.render(context,request)
        rendering_div += '</div'
    return HttpResponse(json.dumps({'result': rendering_div}))
