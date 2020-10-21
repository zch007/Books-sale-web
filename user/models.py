from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 't_user'


class Harvest(models.Model):
    id = models.IntegerField(primary_key=True)
    people = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=100)
    post_code = models.IntegerField()
    phone_number = models.IntegerField(blank=True, null=True)
    tele_number = models.IntegerField(blank=True, null=True)
    harvest_uid = models.ForeignKey(User, models.DO_NOTHING, db_column='harvest_uid')

    class Meta:
        managed = False
        db_table = 't_harvest'
