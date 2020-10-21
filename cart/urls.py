from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_book/', views.add_book, name='add_book'),
    path('remove_book/', views.remove_book, name='remove_book'),
]