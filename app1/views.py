from django.shortcuts import render, redirect
from .models import Contact, Register, Book, Cart, Wishlist, Order_details, Transaction,Offer_banner
import random
from django.core.mail import send_mail
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# @csrf_exempt
# def createpayment(request):
#     if request.session:
#         user = Register.objects.get(email=request.session['email'])
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for i in cart:
#             price = int(i.book.book_price)
#             quantity = int(i.book.quantity)
#             amount = amount + int(price * quantity)
#         stripe.api_key = 'sk_test_51HJZqNBupVwDcjGlTpdPenxFJIPyjjf0U7MIthBbdkyJBqLeFCguM6aAtrEFALeg9OasIjbyLvLjetFaXFcL1eJx00WNCXtlQ4'
#         if request.method == "POST":
#             data = json.loads(request.body)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency=data['currency'],
#                 metadata={'integration_check': 'accept_a_payment'},
#             )
#             try:
#                 return JsonResponse({'publishableKey':
#                                          'pk_test_51HJZqNBupVwDcjGlDVP3kK31TkJPIPcM33wWqCvpj62P7O9uREqEouYAxlsVzsT83YVCzCH4dhUdoYuw3eWUzb1l00RKdKZJ1A',
#                                      'clientSecret': intent.client_secret})
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=403)
#
#
# def checkout(request):
#     if request.session:
#         user = Register.objects.get(email=request.session['email'])
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for i in cart:
#             price = int(i.book.book_price)
#             quantity = int(i.book.quantity)
#             amount = amount + int(price * quantity)
#         return render(request, "app1/checkout.html", {"cart": cart, "total": amount})
#     else:
#         redirect("/login/")
#
#
# def paymentcomplete(request):
#     if request.method == "POST":
#         data = json.loads(request.POST.get("payload"))
#         if data["status"] == "succeeded":
#             msg = "success"
#             return render(request, "app1/index.html", {'msg': msg})


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            return render(request, 'app1/callback.html', context=received_data)
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app1/callback.html', context=received_data)


def initiate_payment(request):
    if request.method == "GET":
        user = Register.objects.get(email=request.session['email'])
        my_cart = Cart.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in my_cart:
            price = int(i.book.book_price)
            quantity = int(i.book.quantity)
            amount = amount + int(price * quantity)
        return render(request, 'app1/order_detail_extra.html',
                      {'user': user, 'cart': cart, 'amount': amount})
    try:
        user = Register.objects.get(email=request.session['email'])
        my_cart = Cart.objects.filter(user=user)
        amount = 0
        for i in my_cart:
            price = int(i.book.book_price)
            quantity = int(i.book.quantity)
            amount = amount + int(price * quantity)
        name = request.POST['uname']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        email = request.POST['email']
        order_email = request.session['email']
        Order_details.objects.create(user=user, name=name, mobile=mobile, address=address, city=city, state=state,
                                     amount=amount, zip_code=zip_code, email=email, order_email=order_email)
    except:
        msg = "Invalid detail"
        user = Register.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=user)
        my_cart = Cart.objects.filter(user=user)
        amount = 0
        for i in my_cart:
            price = int(i.book.book_price)
            quantity = int(i.book.quantity)
            amount = amount + int(price * quantity)
        return render(request, 'app1/order_detail_extra.html',
                      {'user': user, 'cart': cart, 'msg': msg, 'amount': amount})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        ('EMAIL', request.session['email']),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'app1/redirect.html', context=paytm_params)


def order_details(request):
    user = Register.objects.get(email=request.session['email'])
    my_cart = Cart.objects.all()
    amount = 0
    for i in my_cart:
        price = int(i.book.book_price)
        quantity = int(i.book.quantity)
        amount = amount + int(price * quantity)
    if request.method == 'POST':
        print("from Post method")
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        email = request.POST['email']
        order_email = request.session['email']
        Order_details.objects.create(user=user, name=name, mobile=mobile, address=address, city=city, state=state,
                                     amount=amount, zip_code=zip_code, email=email, order_email=order_email)
        msg = "Order details successfully submitted "
        cart = Cart.objects.filter(user=user)
        return render(request, 'app1/order_detail_extra.html', {'msg': msg, 'cart': cart, 'amount': amount})
    else:
        print("from Get Method ")
        cart = Cart.objects.filter(user=user)
        return render(request, 'app1/order_detail_extra.html', {'user': user, 'cart': cart, 'amount': amount})


def index(request):
    try:
        if request.session:
            user = Register.objects.get(email=request.session['email'])
            if user.account_type == 'seller':
                return render(request, 'app1/seller_index.html')
            else:
                return render(request, 'app1/index.html')
        else:
            return render(request, 'app1/index.html')
    except:
        return render(request, 'app1/index.html')


def python(request):
    book = Book.objects.filter(book_status='active')
    return render(request, 'app1/python.html', {'book': book})


def java(request):
    book = Book.objects.filter(book_status='active')
    return render(request, 'app1/java.html', {'book': book})


def php(request):
    book = Book.objects.filter(book_status='active')
    return render(request, 'app1/php.html', {'book': book})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        remarks = request.POST['remarks']
        contacts = Contact.objects.all().order_by('-id')[:10]
        length = len(mobile)
        if email == "":
            msg1 = "Email field is null."
            return render(request, 'app1/contact.html', {'msg1': msg1, 'contacts': contacts})
        elif Contact.objects.filter(email=email).exists():
            msg2 = "This Email already exist."
            return render(request, 'app1/contact.html', {'msg2': msg2, 'contacts': contacts})
        elif Contact.objects.filter(mobile=mobile).exists():
            msg3 = "This Mobile number already exist."
            return render(request, 'app1/contact.html', {'msg3': msg3, 'contacts': contacts})
        elif mobile == "" or length != 10:
            msg4 = "Invalid Mobile number"
            return render(request, 'app1/contact.html', {'msg4': msg4, 'contacts': contacts})
        else:
            msg = "Thank you for contacting us.we'll reply as soon as possible"
            Contact.objects.create(name=name, email=email, mobile=mobile, remarks=remarks)
            return render(request, 'app1/contact.html', {'msg': msg, 'contacts': contacts})
    else:
        contacts = Contact.objects.all().order_by('-id')[:10]
        return render(request, 'app1/contact.html', {'contacts': contacts})


def about(request):
    return render(request, 'app1/about.html')


def register(request):
    user = Register()
    if request.method == 'POST':
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.account_type = request.POST['account_type']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']
        user.pas = request.POST['pas']
        user.cpas = request.POST['cpas']
        user.image = request.FILES['user_image']
        length = len(user.mobile)
        l2 = len(user.pas)
        msg = "User successfully Signed Up"
        if user.pas != user.cpas:
            msg1 = "password and confirm password must be same"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif user.fname == "":
            msg1 = "Please Enter First name"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif user.lname == "":
            msg1 = "Please Enter last name"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif user.pas == "":
            msg1 = "Please Enter password"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif l2 < 8 or l2 > 16:
            msg1 = "Please Enter password between 8 character to 16 character"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif user.mobile == "":
            msg1 = "Please Enter Mobile number"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif length != 10:
            msg1 = "Please Enter Valid Mobile number"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif Register.objects.filter(mobile=user.mobile).exists():
            msg1 = "Mobile number already exist."
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif user.email == "":
            msg1 = "Please Enter Email"
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        elif Register.objects.filter(email=user.email).exists():
            msg1 = "This Email already exist."
            return render(request, 'app1/register.html', {'msg1': msg1, 'user': user})
        else:
            Register.objects.create(fname=user.fname, lname=user.lname, account_type=user.account_type,
                                    email=user.email, mobile=user.mobile, user_image=user.image, pas=user.pas,
                                    cpas=user.cpas)
            rec = [user.email, ]
            otp = random.randint(10000, 99999)
            subject = "OTP For Registration"
            message = "Your OTP for your registration is " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, rec)
            if user.account_type == 'user':
                data = "data"
                return render(request, 'app1/otp.html', {'otp': otp, 'email': user.email, 'data': data})
            else:
                return render(request, 'app1/otp.html', {'otp': otp, 'email': user.email})
    else:
        return render(request, 'app1/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pas = request.POST['pas']
        try:
            user = Register.objects.get(email=email, pas=pas)
            if user.status == 'active' and user.account_type == 'seller':
                request.session['fname'] = user.fname + ' ' + user.lname
                request.session['email'] = user.email
                request.session['image'] = user.user_image.url
                return render(request, 'app1/seller_index.html', {'user': user})
            elif user.status == 'active' and user.account_type == 'user':
                request.session['fname'] = user.fname + ' ' + user.lname
                request.session['email'] = user.email
                request.session['image'] = user.user_image.url
                user1 = Register.objects.get(email=request.session['email'])
                cart_item = Cart.objects.filter(user=user1)
                request.session['count_cart'] = cart_item.count()
                wish1 = Wishlist.objects.filter(user=user1)
                request.session['count_wish'] = wish1.count()
                return render(request, 'app1/index.html', {'user': user})
            else:
                msg = 'Please verify otp before login'
                return render(request, 'app1/enter_email.html', {'msg': msg})
        except:
            msg = "Email or Password incorrect"
            return render(request, 'app1/login.html', {'msg': msg})
    else:
        return render(request, 'app1/login.html')


def verify_otp(request):
    otp = request.POST['otp']
    u_otp = request.POST['u_otp']
    email = request.POST['email']
    if otp == u_otp:
        try:
            if request.session:
                print(email)
                user = Register.objects.get(email=request.session['email'])
                user.email = email
                user.save()
                request.session['email'] = email
                print(request.session['email'])
                if user.account_type == "seller":
                    msg = "Profile Successfully Updated"
                    return render(request, 'app1/profile.html', {'msg': msg, 'user': user})
                else:
                    msg = "Profile Successfully Updated"
                    data = "data"
                    return render(request, 'app1/profile.html', {'msg': msg, 'user': user, 'data': data})

        except Exception as e:
            print(e)
            user = Register.objects.get(email=email)
            if user.status == 'active':
                return render(request, 'app1/forgot_password.html', {'email': email})
            else:
                user.status = 'active'
                user.save()
                msg1 = "You have Successfully signed up.."
                return render(request, 'app1/login.html', {'msg1': msg1})
    else:
        msg1 = "You have entered wrong otp please try again"
        return render(request, 'app1/otp.html', {'msg1': msg1})


def send_otp(request):
    email = request.POST['email']
    try:
        user = Register.objects.get(email=email)
        if user:
            rec = [email, ]
            otp = random.randint(10000, 99999)
            subject = "OTP For Validation"
            message = "Your OTP for your registration is " + str(otp)
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, rec)
            if user.account_type == 'user':
                data = "data"
                return render(request, 'app1/otp.html', {'otp': otp, 'email': email, 'data': data})
            else:
                return render(request, 'app1/otp.html', {'otp': otp, 'email': email})
    except:
        msg = "This email does not exist"
        return render(request, 'app1/login.html', {'msg': msg})


def logout(request):
    user = Register.objects.get(email=request.session['email'])
    try:
        if request.session:
            if user.account_type == 'user':
                del request.session['fname']
                del request.session['email']
                del request.session['image']
                del request.session['count_cart']
                del request.session['count_wish']
                return render(request, 'app1/login.html')
            else:
                del request.session['fname']
                del request.session['email']
                del request.session['image']
                return render(request, 'app1/login.html')
        else:
            return render(request, 'app1/login.html')
    except:
        pass


def enter_email(request):
    return render(request, 'app1/enter_email.html')


def forgot_password(request):
    email = request.POST['email']
    pas = request.POST['pas']
    cpas = request.POST['cpas']
    if pas == cpas:
        try:
            user = Register.objects.get(email=email)
            user.pas = pas
            user.cpas = cpas
            user.save()
            msg1 = "Password updated successfully.."
            return render(request, 'app1/login.html', {'msg1': msg1})
        except:
            pass
    else:
        msg = "Password and Confirm password must be same.."
        return render(request, 'app1/login.html', {'msg': msg})


def change_password(request):
    if request.method == 'POST':
        user = Register.objects.get(email=request.session['email'])
        o_pass = request.POST['o_pas']
        pas = request.POST['pas']
        cpas = request.POST['cpas']
        if o_pass != user.pas:
            msg = "Please enter correct old password"
            if user.account_type == 'seller':
                data = "data"
                return render(request, 'app1/change_password.html', {'msg': msg, 'data': data})
            else:
                return render(request, 'app1/change_password.html', {'msg': msg})
        elif pas != cpas:
            msg = "Password and confirm password must be same"
            if user.account_type == 'seller':
                data = "data"
                return render(request, 'app1/change_password.html', {'msg': msg, 'data': data})
            else:
                return render(request, 'app1/change_password.html', {'msg': msg})
        else:
            user.pas = pas
            user.cpas = cpas
            user.save()
            try:
                if user.account_type == 'seller':
                    del request.session['fname']
                    del request.session['email']
                    del request.session['image']
                    msg1 = "Password successfully updated please login again"
                    return render(request, 'app1/login.html', {'msg1': msg1})
                else:
                    del request.session['fname']
                    del request.session['email']
                    del request.session['image']
                    del request.session['count_cart']
                    del request.session['count_wish']
                    msg1 = "Password successfully updated please login again"
                    return render(request, 'app1/login.html', {'msg1': msg1})
            except:
                pass
    else:
        user = Register.objects.get(email=request.session['email'])
        if user.account_type == 'seller':
            data = "data"
            return render(request, 'app1/change_password.html', {'data': data})
        else:
            return render(request, 'app1/change_password.html')


def add_books(request):
    if request.method == 'POST':
        bc = request.POST['b_category']
        bn = request.POST['b_name']
        bp = request.POST['b_price']
        ba = request.POST['b_author']
        bd = request.POST['b_desc']
        bi = request.FILES['b_image']
        seller_email = request.session['email']
        Book.objects.create(book_name=bn, book_price=bp, book_category=bc, book_desc=bd, book_author=ba, book_image=bi,
                            seller_email=seller_email)
        msg = "Book added successfully"
        return render(request, 'app1/add_books.html', {'msg': msg})
    else:
        return render(request, 'app1/add_books.html')


def view_books(request):
    email = request.session['email']
    books = Book.objects.filter(book_status="active", seller_email=request.session['email'])
    return render(request, 'app1/view_books.html', {'books': books, 'email': email})


def more_details(request, pk):
    books = Book.objects.get(pk=pk)
    user = Register.objects.get(email=request.session['email'])
    try:
        if user.account_type == 'user':
            data = "user"
            return render(request, 'app1/more_details.html', {'books': books, 'data': data, 'user': user})
        else:
            return render(request, 'app1/more_details.html', {'books': books, 'user': user})
    except:
        pass


def remove_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.book_status = "inactive"
    book.save()
    books = Book.objects.filter(book_status='active', seller_email=request.session['email'])
    msg = "Book deleted successfully"
    return render(request, 'app1/view_books.html', {'msg': msg, 'books': books})


def help_me(request):
    return render(request, 'app1/help.html')


def search_book(request):
    search = request.POST['search']
    books = Book.objects.filter(seller_email=request.session['email'], book_status='active', book_name__contains=search)
    return render(request, 'app1/view_books.html', {'books': books})


def inactive_books(request):
    books = Book.objects.filter(book_status='inactive', seller_email=request.session['email'])
    return render(request, 'app1/inactive_books.html', {'books': books})


def active_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.book_status = "active"
    book.save()
    msg = "Book active successfully"
    books = Book.objects.filter(book_status='inactive')
    return render(request, 'app1/inactive_books.html', {'msg': msg, 'books': books})


def add_cart(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        user = Register.objects.get(email=request.session['email'])
        try:
            wish1 = Wishlist.objects.get(book=book)
            wish1.delete()
            a = Cart.objects.filter(book=book)
            if a:
                book.quantity = int(book.quantity) + 1
                cart = Cart.objects.filter(user=user)
                msg = "Add to Cart Successfully"
                return render(request, 'app1/view_cart.html', {'cart': cart, 'msg': msg})
            else:
                Cart.objects.create(user=user, book=book)
                book.quantity = 1
                book.save()
                cart = Cart.objects.filter(user=user)
                request.session['count_cart'] = cart.count()
                wish1 = Wishlist.objects.filter(user=user)
                request.session['count_wish'] = wish1.count()
                msg = "Add to Cart Successfully"
                return render(request, 'app1/view_cart.html', {'cart': cart, 'msg': msg})
        except:
            a = Cart.objects.filter(book=book)
            if a:
                book.quantity = int(book.quantity) + 1
                book.save()
                cart = Cart.objects.filter(user=user)
                msg = "Add to Cart Successfully"
                return render(request, 'app1/view_cart.html', {'cart': cart, 'msg': msg})
            else:
                Cart.objects.create(user=user, book=book)
                cart = Cart.objects.filter(user=user)
                book.quantity = 1
                book.save()
                request.session['count_cart'] = cart.count()
                msg = "Add to Cart Successfully"
                return render(request, 'app1/view_cart.html', {'cart': cart, 'msg': msg})
    except:
        msg = "Please Login Again for this function"
        return render(request, 'app1/login.html', {'msg': msg})


def view_cart(request):
    user = Register.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user)
    my_cart = Cart.objects.all()
    amount = 0
    for i in my_cart:
        price = int(i.book.book_price)
        quantity = int(i.book.quantity)
        amount = amount + int(price * quantity)
    msg2 = "Cart Empty"
    return render(request, 'app1/view_cart.html', {'cart': cart, 'msg2': msg2, 'amount': amount})


def remove_cart(request, pk):
    book = Book.objects.get(pk=pk)
    user = Register.objects.get(email=request.session['email'])
    cart1 = Cart.objects.get(book=book)
    book.quantity = 1
    book.save()
    cart1.delete()
    cart = Cart.objects.filter(user=user)
    request.session['count_cart'] = cart.count()
    msg = "book removed from cart"
    msg2 = "No item left from Cart"
    return render(request, 'app1/view_cart.html', {'msg': msg, 'cart': cart, 'msg2': msg2})


def add_wishlist(request, pk):
    book = Book.objects.get(pk=pk)
    user = Register.objects.get(email=request.session['email'])
    cart1 = Cart.objects.get(book=book)
    cart1.delete()
    cart = Cart.objects.filter(user=user)
    request.session['count_cart'] = cart.count()
    Wishlist.objects.create(user=user, book=book)
    wish = Wishlist.objects.filter(user=user)
    request.session['count_wish'] = wish.count()
    msg = "Add to Wishlist Successfully"
    return render(request, 'app1/wishlist.html', {'wish': wish, 'msg': msg})


def wishlist(request):
    user = Register.objects.get(email=request.session['email'])
    wish = Wishlist.objects.filter(user=user)
    request.session['count_wish'] = wish.count()
    return render(request, 'app1/wishlist.html', {'wish': wish})


def remove_wish(request, pk):
    book = Book.objects.get(pk=pk)
    user = Register.objects.get(email=request.session['email'])
    wish1 = Wishlist.objects.get(book=book)
    wish1.delete()
    wish = Wishlist.objects.filter(user=user)
    request.session['count_wish'] = wish.count()
    msg = "book removed from wishlist"
    return render(request, 'app1/wishlist.html', {'msg': msg, 'wish': wish})


def profile(request):
    user = Register.objects.get(email=request.session['email'])
    try:
        if request.method == 'POST':
            fname1 = request.POST['fname1']
            lname1 = request.POST['lname1']
            mobile1 = request.POST['mobile1']
            email = request.POST['email']
            try:
                if user.email != email and Register.objects.filter(email=email).exists():
                    if user.account_type == 'user':
                        msg1 = "Email Already Exist choose different email"
                        data = 'data'
                        return render(request, 'app1/profile.html', {'user': user, 'msg1': msg1, 'data': data})
                    else:
                        msg1 = "Email Already Exist choose different email"
                        return render(request, 'app1/profile.html', {'user': user, 'msg1': msg1})
                elif user.email != email:
                    try:
                        image1 = request.FILES['userimage']
                        user.fname = fname1
                        user.lname = lname1
                        user.mobile = mobile1
                        user.user_image = image1
                        user.save()
                        request.session['fname'] = user.fname
                        request.session['image'] = user.user_image.url
                        rec = [email, ]
                        otp = random.randint(10000, 99999)
                        subject = "OTP For Registration"
                        message = "Your OTP for your registration is " + str(otp)
                        email_from = settings.EMAIL_HOST_USER
                        send_mail(subject, message, email_from, rec)
                        if user.account_type == 'user':
                            data = "data"
                            return render(request, 'app1/otp.html', {'otp': otp, 'email': email, 'data': data})
                        else:
                            return render(request, 'app1/otp.html', {'otp': otp, 'email': email})
                    except:
                        user.fname = fname1
                        user.lname = lname1
                        user.mobile = mobile1
                        user.save()
                        request.session['fname'] = user.fname
                        rec = [email, ]
                        otp = random.randint(10000, 99999)
                        subject = "OTP For Registration"
                        message = "Your OTP for your registration is " + str(otp)
                        email_from = settings.EMAIL_HOST_USER
                        send_mail(subject, message, email_from, rec)
                        if user.account_type == 'user':
                            data = "data"
                            return render(request, 'app1/otp.html', {'otp': otp, 'email': email, 'data': data})
                        else:
                            return render(request, 'app1/otp.html', {'otp': otp, 'email': email})
                else:
                    image1 = request.FILES['userimage']
                    user.fname = fname1
                    user.lname = lname1
                    user.mobile = mobile1
                    user.email = email
                    user.user_image = image1
                    user.save()
                    request.session['fname'] = user.fname
                    request.session['image'] = user.user_image.url
                    msg = "profile successfully updated."
                    if user.account_type == 'user':
                        data = 'data'
                        return render(request, 'app1/profile.html', {'user': user, 'msg': msg, 'data': data})
                    else:
                        return render(request, 'app1/profile.html', {'user': user, 'msg': msg})
            except:
                user.fname = fname1
                user.lname = lname1
                user.mobile = mobile1
                user.save()
                request.session['fname'] = user.fname
                msg = "profile successfully updated."
                if user.account_type == 'user':
                    data = 'data'
                    return render(request, 'app1/profile.html', {'user': user, 'msg': msg, 'data': data})
                else:
                    return render(request, 'app1/profile.html', {'user': user, 'msg': msg})
        else:
            if user.account_type == 'user':
                data = 'data'
                return render(request, 'app1/profile.html', {'user': user, 'data': data})
            else:
                return render(request, 'app1/profile.html', {'user': user})
    except:
        pass


def all_book(request):
    book = Book.objects.filter(book_status='active')
    return render(request, 'app1/all_book.html', {'book': book})


def sort1(request):
    sort = Book.objects.all().order_by('book_name')
    return render(request, 'app1/all_book.html', {'sort': sort})


def sort2(request):
    sort = Book.objects.filter(book_status='active').order_by('-book_name')
    return render(request, 'app1/all_book.html', {'sort': sort})


def sort3(request):
    sort = Book.objects.filter(book_status='active').order_by('book_price')
    return render(request, 'app1/all_book.html', {'sort': sort})


def sort4(request):
    sort = Book.objects.filter(book_status='active').order_by('-book_price')
    return render(request, 'app1/all_book.html', {'sort': sort})


def filter1(request):
    if request.method == 'POST':
        p1 = request.POST['price1']
        p2 = request.POST['price2']
        ft = Book.objects.filter(book_price__range=(p1, p2), book_status='active')
        if not ft:
            msg3 = "No book Found at this Range of Price"
            return render(request, 'app1/all_book.html', {'ft': ft, 'msg3': msg3})
        else:
            return render(request, 'app1/all_book.html', {'ft': ft})
    else:
        book = Book.objects.filter(book_status='active')
        return render(request, 'app1/all_book.html', {'book': book})


def user_more_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'app1/user_more_detail.html', {'book': book})


def remove_checkout(request, pk):
    user = Register.objects.get(email=request.session['email'])
    my_cart = Cart.objects.get(pk=pk)
    my_cart.delete()
    cart = Cart.objects.filter(user=user)
    request.session['count_cart'] = cart.count()
    amount = 0
    for i in cart:
        price = int(i.book.book_price)
        quantity = int(i.book.quantity)
        amount = amount + int(price * quantity)
    return render(request, 'app1/order_detail_extra.html', {'user': user, 'cart': cart, 'amount': amount})


def my_orders(request):
    user = Register.objects.get(email=request.session['email'])
    orders = Order_details.objects.filter(order_email=user.email)
    return render(request, 'app1/orders.html', {'orders': orders})

