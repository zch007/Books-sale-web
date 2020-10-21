from index.models import Book


class Book0:  # 自定义一个书籍类，用于模拟本地数据库
    def __init__(self, id, count):
        book = Book.objects.get(id=id)
        self.id = id
        self.count = count
        self.name = book.book_name
        self.price = book.dangdang_price
        self.origin_price = book.origin_price
        self.pic = book.main_pic
        self.description = book.bookdisplay_set.get().media_comment

    def total_price(self):
        return '%.2f' % (float(float(self.price) * float(self.count)))


class Cart:  # 自定义本地购物车
    def __init__(self):
        self.booklist = []

    def get_book(self, id):
        for book in self.booklist:
            if book.id == id:
                return book

    def add_book(self, id, count):
        book = self.get_book(id)
        if book:
            book.count = int(book.count) + int(count)
        else:
            book = Book0(id=id, count=count)
            self.booklist.append(book)

    def remove_book(self, id):
        book = self.get_book(id)
        self.booklist.remove(book)
