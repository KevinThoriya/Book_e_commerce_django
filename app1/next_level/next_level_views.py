from django.shortcuts import render, redirect
from app1.models import Contact, Register, Book, Cart, Wishlist, Order_details, Transaction

def index(request):
    return render(request,'app1/next_level/index.html')