from django.urls import path
from order import views

app_name = 'order'
urlpatterns = [
    path('order/', views.order, name='order'),
    path('order_ok/', views.order_ok, name='order_ok'),
    path('order_submit/', views.order_submit, name='order_submit'),
    path('put_off/', views.put_off, name='put_off'),
    path('order_list/', views.order_list, name='order_list'),
]