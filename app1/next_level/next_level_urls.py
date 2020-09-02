from django.urls import path
from . import next_level_views as views

base_url = 'next_level/'
urlpatterns = [
    path(base_url + '',views.index,name="home_n"),
    path(base_url + 'product/',views.product_detail,name="product_detail_n"),
    path(base_url + 'about/',views.about_us,name="about_n"),
    path(base_url + 'services/',views.services,name="services_n"),
    path(base_url + 'books/',views.book_list,name="books_n"),
    path(base_url + 'welcome/',views.login_signup,name="log_sign_n"),

]

