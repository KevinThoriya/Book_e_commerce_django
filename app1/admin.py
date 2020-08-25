from django.contrib import admin
from .models import Contact,Register,Book,Cart, Wishlist, Order_details, Transaction

admin.site.register(Contact)
admin.site.register(Register)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order_details)
admin.site.register(Transaction)

# Register your models here.
