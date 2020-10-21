from django.db import models
from index.models import Book
from user.models import Harvest, User


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    origin_address = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    carriage = models.IntegerField()
    order_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='order_uid')
    order_hid = models.ForeignKey(Harvest, models.DO_NOTHING, db_column='order_hid')

    class Meta:
        managed = False
        db_table = 't_order'


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    order_item_oid = models.ForeignKey(Order, models.DO_NOTHING, db_column='order_item_oid')
    order_item_bid = models.ForeignKey(Book, models.DO_NOTHING, db_column='order_item_bid')

    class Meta:
        managed = False
        db_table = 't_order_item'
