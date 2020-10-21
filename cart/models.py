from django.db import models
from index.models import Book
from user.models import User


class Cart(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    cart_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='cart_uid')
    cart_bid = models.ForeignKey(Book, models.DO_NOTHING, db_column='cart_bid')

    class Meta:
        managed = False
        db_table = 't_cart'
