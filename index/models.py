from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    level = models.IntegerField()
    parent_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_category'


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=20)
    main_pic = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    publish_date = models.DateField()
    origin_price = models.IntegerField()
    dangdang_price = models.IntegerField()
    number = models.IntegerField()
    traffic = models.IntegerField()
    comment_number = models.IntegerField()
    book_cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='book_cid')

    def discount(self):
        return '%.2f' % (float(self.dangdang_price) / float(self.origin_price) * 10.0)

    class Meta:
        managed = False
        db_table = 't_book'


class BookDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    page_number = models.IntegerField()
    word_number = models.IntegerField()
    print_date = models.DateField()
    format = models.IntegerField()
    page_type = models.CharField(max_length=10)
    print_number = models.IntegerField()
    pack_type = models.CharField(max_length=10)
    is_suit = models.IntegerField()
    isbn = models.IntegerField()
    book_detail_bid = models.ForeignKey(Book, models.DO_NOTHING, db_column='book_detail_bid')

    class Meta:
        managed = False
        db_table = 't_book_detail'


class BookDisplay(models.Model):
    id = models.IntegerField(primary_key=True)
    editor_recommend = models.CharField(max_length=100)
    content_recommend = models.CharField(max_length=100)
    author_summarize = models.CharField(max_length=100)
    media_comment = models.CharField(max_length=100)
    part_content = models.CharField(max_length=200)
    book_display_bid = models.ForeignKey(Book, models.DO_NOTHING, db_column='book_display_bid')

    class Meta:
        managed = False
        db_table = 't_book_display'


class Pic(models.Model):
    id = models.IntegerField(primary_key=True)
    pic_1 = models.CharField(max_length=50)
    pic_2 = models.CharField(max_length=50)
    pic_3 = models.CharField(max_length=50)
    pic_4 = models.CharField(max_length=50)
    pic_5 = models.CharField(max_length=50)
    pic_bid = models.ForeignKey(Book, models.DO_NOTHING, db_column='pic_bid')

    class Meta:
        managed = False
        db_table = 't_pic'
