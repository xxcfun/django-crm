from django.db import models

# Create your models here.
from customer.models import Customer
from users.models import User
from utils import constants


class Business(models.Model):
    """客户商机"""
    name = models.CharField(verbose_name='商机名称', max_length=64)
    customer = models.ForeignKey(Customer, verbose_name='商机客户', on_delete=models.CASCADE)
    winning_rate = models.SmallIntegerField(verbose_name='赢单率', choices=constants.BUSINESS_WINNING, default=constants.WINNING_ERSHI)
    money = models.CharField(verbose_name='预估金额', max_length=16, blank=True, null=True)
    remarks = models.CharField(verbose_name='商机备注', max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='创建人', related_name='customer_business', on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)

    class Meta:
        db_table = 'business'
        verbose_name = verbose_name_plural = "客户商机"

    def __str__(self):
        return self.name
