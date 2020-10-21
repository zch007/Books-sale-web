from django.urls import path
from index import views

app_name = 'index'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('booklist/<pk>/', views.booklist, name='booklist'),
    path('details/<pk>/', views.details, name='details'),
    path('safe_exit/', views.safe_exit, name='safe_exit'),
]
