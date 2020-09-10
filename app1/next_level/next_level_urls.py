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
    path(base_url + 'update_profile/',views.update_profile,name="update_profile_n"),
    path(base_url + 'manage/product_and_order/',views.manage_product_order,name="manage_book_order_n"),
    path(base_url + 'my_order/',views.my_order,name="view_my_order_n"),
    path(base_url + 'manage/edit_book/',views.manage_edit_book,name="manage_edit_book_n"),
    
]+[
    path(base_url + 'product_view/',views.product_view,name="product_detail_view_n"),
    path(base_url + 'sign_up_form/',views.sign_up_form,name="sign_up_form_n"),
    path(base_url + 'books/filter/', views.book_filter, name="book_filter_n")
]
