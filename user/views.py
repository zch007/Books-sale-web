from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from captcha.image import ImageCaptcha
from index.models import Book
from user.models import User
from cart.models import Cart
import random
import string


def register(request):
    return_url = request.GET.get('return_url')
    id = request.GET.get('id')
    return render(request, 'user/register.html', {'return_url': return_url, 'id': id})


def login(request):
    return_url = request.GET.get('return_url')
    id = request.GET.get('id')
    return render(request, 'user/login.html', {'return_url': return_url, 'id': id})


def register_ok(request):
    user = request.session.get('user')
    return_url = request.GET.get('return_url')
    id = request.GET.get('id')
    return render(request, 'user/register ok.html', {'user': user, 'return_url': return_url, 'id': id})


def register_logic(request):
    try:
        user_name = request.POST.get('txt_username')
        user_pwd = request.POST.get('txt_password')
        name = request.POST.get('txt_name')
        code = request.POST.get('txt_vcode')
        if code.lower() == request.session.get('code').lower():
            if User.objects.filter(user_name=user_name):
                return HttpResponse('此手机号或邮箱已注册')
            else:
                with transaction.atomic():
                    User.objects.create(user_name=user_name, user_pwd=user_pwd, name=name)
                    user = User.objects.get(user_name=user_name)
                    request.session['user'] = user
                    # 注册状态还需将session中的书传到数据库中
                    local_cart = request.session.get('cart')
                    if local_cart:
                        for book in local_cart.booklist:
                            id = book.id
                            count = book.count
                            book = Book.objects.get(id=id)  # 书籍库中的原书
                            book0 = Cart.objects.filter(cart_uid=user.id, cart_bid=id)  # 检验用户购物车中是否有该书
                            if book0:
                                with transaction.atomic():
                                    book0[0].number += int(count)
                                    book0[0].save()
                            else:
                                with transaction.atomic():
                                    Cart.objects.create(number=count, cart_uid=user, cart_bid=book)
                        with transaction.atomic():
                            del request.session['cart']
                    return redirect('user:register_ok')
        return HttpResponse('验证码错误')
    except Exception as e:
        print(e)
        return HttpResponse('提交错误，请检查')


def login_logic(request):
    try:
        user_name = request.POST.get('user_name')
        user_pwd = request.POST.get('user_pwd')
        code = request.POST.get('code')
        checked = request.POST.get('checked')
        if code.lower() == request.session.get('code').lower():
            if User.objects.filter(user_name=user_name, user_pwd=user_pwd):
                user = User.objects.get(user_name=user_name)
                request.session['user'] = user
                if checked == 'true':
                    resp = HttpResponse('OK')
                    resp.set_cookie('uid', user.id, max_age=(7 * 24 * 3600))
                    # 登陆状态还需将session中的书传到数据库中
                    local_cart = request.session.get('cart')
                    if local_cart:
                        for book in local_cart.booklist:
                            id = book.id
                            count = book.count
                            book = Book.objects.get(id=id)  # 书籍库中的原书
                            book0 = Cart.objects.filter(cart_uid=user.id, cart_bid=id)  # 检验用户购物车中是否有该书
                            if book0:
                                with transaction.atomic():
                                    book0[0].number += int(count)
                                    book0[0].save()
                            else:
                                with transaction.atomic():
                                    Cart.objects.create(number=count, cart_uid=user, cart_bid=book)
                        with transaction.atomic():
                            del request.session['cart']
                    return resp
                else:
                    # 登陆状态还需将session中的书传到数据库中
                    local_cart = request.session.get('cart')
                    if local_cart:
                        for book in local_cart.booklist:
                            id = book.id
                            count = book.count
                            book = Book.objects.get(id=id)  # 书籍库中的原书
                            book0 = Cart.objects.filter(cart_uid=user.id, cart_bid=id)  # 检验用户购物车中是否有该书
                            if book0:
                                with transaction.atomic():
                                    book0[0].number += int(count)
                                    book0[0].save()
                            else:
                                with transaction.atomic():
                                    Cart.objects.create(number=count, cart_uid=user, cart_bid=book)
                        with transaction.atomic():
                            del request.session['cart']
                    return redirect('index:index')
            else:
                return HttpResponse('用户名或密码错误')
        return HttpResponse('验证码错误')
    except Exception as e:
        print(e)
        return HttpResponse('提交错误，请检查')


def get_captcha(request):
    image = ImageCaptcha()
    code_list = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 4)
    code = ''.join(code_list)
    print(code)
    request.session['code'] = code
    data = image.generate(code)
    return HttpResponse(data, 'img/png')
