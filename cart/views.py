from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from cart.cart import Cart
from cart.models import Cart as U_cart
from index.models import Book
from user.models import User


def cart(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    try:
        if user:  # 登录
            # 显示用户购物车中的数据
            my_cart = U_cart.objects.filter(cart_uid=user.id)
            cart = []
            for book in my_cart:  # 遍历数据库中的购物车对象
                id = book.cart_bid.id
                count = book.number
                name = book.cart_bid.book_name
                price = book.cart_bid.dangdang_price
                origin_price = book.cart_bid.origin_price
                pic = book.cart_bid.main_pic
                description = book.cart_bid.bookdisplay_set.get().media_comment
                total_price = '%.2f' % (float(float(price) * float(count)))
                cart.append(
                    {'id': id, 'count': count, 'name': name, 'price': price, 'origin_price': origin_price, 'pic': pic,
                     'description': description, 'total_price': total_price})
        else:  # 未登录
            local_cart = request.session.get('cart')
            cart = []
            if local_cart:
                cart = local_cart.booklist
        return render(request, 'cart/cart.html', {'user': user, 'cart': cart})
    except Exception as e:
        print(e)
        return HttpResponse('出错了')


def add_book(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    id = int(request.GET.get('id'))  # 获取书的id
    count = int(request.GET.get('count'))  # 获取添加书的数量

    try:
        if user:
            book = U_cart.objects.filter(cart_uid=user.id, cart_bid=id)  # 获取购物车中所存放的书
            if book:  # 如果该书存在
                with transaction.atomic():
                    book[0].number += count  # 书的数量变化
                    book[0].save()
            else:  # 不存在
                book = Book.objects.get(id=id)  # 获取到书的对象
                with transaction.atomic():
                    U_cart.objects.create(number=count, cart_uid=user, cart_bid=book)  # 向购物车中添加书
        else:
            local_cart = request.session.get('cart')
            if local_cart:
                pass
            else:
                local_cart = Cart()  # 创建新的本地购物车
            with transaction.atomic():
                local_cart.add_book(id=id, count=count)
                request.session['cart'] = local_cart
        return HttpResponse('已添加' + str(count) + '本书籍')
    except Exception as e:
        print(e)
        return HttpResponse('出错了')


def remove_book(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    id = int(request.GET.get('id'))  # 获取书的id

    try:
        if user:
            book = U_cart.objects.filter(cart_bid=id)
            with transaction.atomic():
                book.delete()
        else:
            local_cart = request.session.get('cart')
            with transaction.atomic():
                local_cart.remove_book(id=id)
                request.session['cart'] = local_cart
        return HttpResponse('ok')
    except Exception as e:
        print(e)
        return HttpResponse('出错了')
