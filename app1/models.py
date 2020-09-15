from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.db.models import Q


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(null=False)
    mobile = models.CharField(max_length=10)
    remarks = models.TextField()

    def __str__(self):
        return self.name


class Register(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    account_type = models.CharField(max_length=20, default="user")
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    pas = models.CharField(max_length=30)
    cpas = models.CharField(max_length=30)
    user_image = models.ImageField(upload_to='images/', default='')
    status = models.CharField(max_length=20, default="inactive")

    def __str__(self):
        return self.fname + " " + self.lname


class Book(models.Model):
    CHOICES = (
        ('python', 'python'),
        ('java', 'java'),
        ('php', 'php')
    )
    book_name = models.CharField(max_length=30)
    book_price = models.CharField(max_length=10)
    book_author = models.CharField(max_length=30)
    book_category = models.CharField(
        max_length=30, choices=CHOICES, default='')
    book_desc = models.TextField()
    book_image = models.ImageField(upload_to='images/')
    book_status = models.CharField(max_length=30, default="active")
    quantity = models.CharField(default=0, max_length=10)
    seller_email = models.EmailField(default='')

    def __str__(self):
        return self.book_name


class Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user.fname + " - " + self.book.book_name


class Wishlist(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user.fname + " - " + self.book.book_name


class Order_details(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    order_email = models.CharField(max_length=50, default="")
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    email = models.EmailField(default="")
    zip_code = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    mobile = models.CharField(max_length=12)
    order_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


class Transaction(models.Model):
    made_by = models.ForeignKey(Register, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime(
                'PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.made_by.fname

def get_expire():
    return datetime.today() + timedelta(days=2)

class Offer_banner(models.Model):
    offer_main_title = models.CharField(max_length=100,null=False)
    offer_sub_title = models.CharField(max_length=100,null=False)
    offer_image = models.ImageField(upload_to='images/')
    offer_redirection_url = models.URLField(null=False)
    offer_active_date = models.DateField(default=datetime.today)
    offer_expire_date = models.DateField(default=get_expire)
    payment_price = models.IntegerField(max_length=10)
    payment = models.BooleanField(default=0)
    expire = models.BooleanField(default=0) 

    def __str__(self):
        return self.offer_main_title

    @staticmethod
    def running_offers(*args,**kwargs):
        active_offer = Offer_banner.objects.filter(payment=True,expire=False).order_by('-payment_price')[:5]
        return active_offer 
       
    # Must Add this in form validation by_yk 
    # widget = forms.SelectDateWidget(years=range(2020, 2100))
