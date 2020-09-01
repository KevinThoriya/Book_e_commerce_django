from django.urls import path
from . import next_level_views as views

base_url = 'next_level'
urlpatterns = [
    path('next_level/home/',views.index,name="home_n"),
    path('next_level/product/',views.product_detail,name="product_detail")
]
