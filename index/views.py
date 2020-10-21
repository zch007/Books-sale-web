from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from index.models import Category, Book
from user.models import User


def index(request):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    cates1 = Category.objects.filter(level=1)  # 用于显示一级分类
    cates2 = Category.objects.filter(level=2)  # 用于显示二级分类

    news = Book.objects.all().order_by('-publish_date')  # 新书上架
    recommends = Book.objects.all().order_by('traffic')  # 主编推荐
    sales = Book.objects.all().order_by('-publish_date').order_by('number')  # 新书热卖

    return render(request, 'index/index.html',
                  {'cates1': cates1, 'cates2': cates2, 'news': news, 'recommends': recommends, 'sales': sales,
                   'user': user})


def booklist(request, pk):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    cate = Category.objects.get(id=pk)  # 用于判断当前分类为一级还是二级
    cates1 = Category.objects.filter(level=1)  # 用于显示一级分类
    cates2 = Category.objects.filter(level=2)  # 用于显示二级分类

    # 获取当前页码（默认为1）
    number = request.GET.get('num', 1)

    # 判断当前分类的级别
    if cate.level == 1:
        if Category.objects.filter(parent_id=cate.id):
            pagtor = Paginator(Book.objects.filter(book_cid__parent_id=pk), per_page=2)  # 获取分类器对象
            c1 = Category.objects.filter(id=pk)  # 用于面包屑展示一级标签
            c2 = ''  # 用于面包屑展示二级标签
        else:
            pagtor = Paginator(Book.objects.filter(book_cid__id=pk), per_page=2)
            c1 = Category.objects.filter(id=pk)
            c2 = ''
    else:
        pagtor = Paginator(Book.objects.filter(book_cid__id=pk), per_page=2)
        c2 = Category.objects.filter(id=pk)
        c1 = Category.objects.filter(id=c2[0].parent_id)

    page_num = pagtor.num_pages  # 获取总页数
    page = pagtor.page(number)

    return render(request, 'index/booklist.html',
                  {'cates1': cates1, 'cates2': cates2, 'c1': c1, 'c2': c2, 'page': page, 'page_num': page_num,
                   'user': user, 'cate': cate})


def details(request, pk):
    # 判断登陆状态
    cookie_uid = request.COOKIES.get('uid')
    user = ''
    if cookie_uid:
        user = User.objects.get(id=cookie_uid)
    else:
        session_user = request.session.get('user')
        if session_user:
            user = session_user

    book = Book.objects.get(id=pk)  # 获取相应图书对象
    c2 = Category.objects.get(id=book.book_cid.id)  # 面包屑

    if c2.id <= 14:
        c1 = ''
    else:
        c1 = Category.objects.get(id=c2.parent_id)

    return render(request, 'index/Book details.html', {'book': book, 'c1': c1, 'c2': c2, 'user': user})


def safe_exit(request):
    response = HttpResponse('安全退出')
    response.set_cookie('uid', max_age=0)  # 清cookie
    request.session.flush()  # 清session
    return response
