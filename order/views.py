from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cart.models import Cart
from index.models import Book
from order.models import Harvest
from cart.cart import Cart as L_cart
from order.models import Order, OrderItem
from user.models import User
import random
import string
import time


def order(request):
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
        my_cart = Cart.objects.filter(cart_uid=user.id)  # 获取该用户的购物车
        cart = []
        total_prices = 0  # 用于累加总价
        counts = 0  # 用于累加总数
        for book in my_cart:
            id = book.cart_bid.id
            count = book.number
            counts = int(counts) + int(count)
            name = book.cart_bid.book_name
            publisher = book.cart_bid.publisher
            price = book.cart_bid.dangdang_price
            origin_price = book.cart_bid.origin_price
            total_price = float(price) * float(count)
            total_prices = float(total_prices) + float(total_price)
            total_price = '%.2f' % total_price
            total_prices = '%.2f' % total_prices
            discount = '%.2f' % (float(price) / float(origin_price) * 10.0)
            cart.append(
                {'id': id, 'count': count, 'name': name, 'publisher': publisher, 'price': price,
                 'origin_price': origin_price, 'total_price': total_price, 'discount': discount})
            # 获取收货地址对象
            harvest = Harvest.objects.filter(harvest_uid=user.id)
        return render(request, 'order/indent.html',
                      {'user': user, 'total_prices': total_prices, 'counts': counts, 'cart': cart, 'harvest': harvest})
    except Exception as e:
        print(e)
        return redirect('cart:cart')


def order_submit(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    try:  # 强制登陆
        # 获取添加到收货地址表的参数
        hid = request.POST.get('hid')
        people = request.POST.get('people')
        detail_address = request.POST.get('detail_address')
        post_code = int(request.POST.get('post_code'))
        post_code = '%06d' % post_code
        phone_number = request.POST.get('phone_number')
        if phone_number == '':
            phone_number = None
        tele_number = request.POST.get('tele_number')
        if tele_number == '':
            tele_number = None
        if hid == '':
            with transaction.atomic():
                Harvest.objects.create(people=people, detail_address=detail_address, post_code=post_code,
                                       phone_number=phone_number, tele_number=tele_number, harvest_uid=user)
                harvest = Harvest.objects.filter(people=people, detail_address=detail_address, post_code=post_code,
                                                 phone_number=phone_number, tele_number=tele_number, harvest_uid=user)[
                    0]
        else:
            harvest = Harvest.objects.get(id=hid)
        # 获取订单完成页面显示的参数
        counts = request.POST.get('counts')
        total_prices = request.POST.get('total_prices')
        # 向数据库订单表中传数据
        order_id_list = random.sample(string.ascii_uppercase + string.digits, 11)
        order_id = ''.join(order_id_list)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        origin_address = '当当自营'
        carriage = 15
        with transaction.atomic():
            Order.objects.create(order_id=order_id, create_time=create_time, origin_address=origin_address,
                                 total_price=float(total_prices), carriage=carriage, order_hid=harvest,
                                 order_uid=user)
        # 创建订单项
        cart = Cart.objects.filter(cart_uid=user.id)
        for book in cart:
            book_object = book.cart_bid
            order = Order.objects.get(order_id=order_id)
            with transaction.atomic():
                OrderItem.objects.create(number=counts, order_item_oid=order, order_item_bid=book_object)
        # 将需要显示的传到session中
        with transaction.atomic():
            request.session['order_id'] = order_id
            request.session['people'] = people
            request.session['counts'] = counts
            request.session['total_prices'] = total_prices
            request.session['phone_number'] = phone_number
            request.session['detail_address'] = detail_address
        # 清空购物车
        with transaction.atomic():
            cart.delete()
        # 将session中的书拿出来放回到购物车中
        local_cart = request.session.get('cart').booklist
        for book in local_cart:
            id = book.id
            book_object = Book.objects.get(id=id)
            count = book.count
            with transaction.atomic():
                Cart.objects.create(cart_bid=book_object, cart_uid=user, number=count)
        del request.session['cart']  # 将本地购物车session清空
        return HttpResponse('ok')
    except Exception as e:
        print(e)
        return redirect('user:login')


def put_off(request):
    # 先将订单中要放回购物车的书放到session中
    id = request.GET.get('id')
    count = request.GET.get('count')
    local_cart = request.session.get('cart')
    if local_cart:
        pass
    else:
        local_cart = L_cart()  # 创建新的本地购物车
    with transaction.atomic():
        local_cart.add_book(id=id, count=count)
        request.session['cart'] = local_cart
        return HttpResponse('已将所选书籍放回到购物车中')


def order_ok(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    order_id = request.session.get('order_id')
    people = request.session.get('people')
    counts = request.session.get('counts')
    total_prices = request.session.get('total_prices')
    detail_address = request.session.get('detail_address')
    phone_number = request.session.get('phone_number')
    if people:  # 判断是否为浏览器输入框手动输入网址
        return render(request, 'order/indent ok.html',
                      {'user': user, 'counts': counts, 'totals_prices': total_prices, 'people': people,
                       'order_id': order_id, 'phone_number': phone_number, 'detail_address': detail_address})
    else:
        return redirect('cart:cart')


def order_list(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    order_id = request.GET.get('order_id')
    order = Order.objects.get(order_id=order_id)
    create_time = order.create_time
    origin_address = order.origin_address
    total_price = order.total_price
    carriage = order.carriage
    count = request.session.get('counts')
    people = request.session.get('people')
    detail_address = request.session.get('detail_address')
    phone_number = request.session.get('phone_number')
    return render(request, 'order/order_list.html',
                  {'user': user, 'order_id': order_id, 'create_time': create_time, 'origin_address': origin_address,
                   'total_price': total_price, 'carriage': carriage, 'count': count, 'detail_address': detail_address,
                   'people': people, 'phone_number': phone_number})
