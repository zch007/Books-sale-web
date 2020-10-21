from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('register_logic/', views.register_logic, name='register_logic'),
    path('register_ok/', views.register_ok, name='register_ok'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
]
