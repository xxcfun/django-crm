from django.db import models

# Create your models here.
from users.models import User
from customer.models import Customer
from utils import constants


class Record(models.Model):
    """客户拜访记录模型"""
    theme = models.CharField(verbose_name='拜访主题', max_length=256)
    customer = models.ForeignKey(Customer, verbose_name='客户', related_name='customer_record', on_delete=models.CASCADE)
    status = models.SmallIntegerField(verbose_name='客户拜访方式', choices=constants.RECORD_STATUS, default=constants.STATUS_XS)
    user = models.ForeignKey(User, verbose_name='创建人', related_name='customer_record', on_delete=models.CASCADE)
    main = models.TextField(verbose_name='主要事宜', max_length=1000, null=True, blank=True)
    next = models.TextField(verbose_name='后期规划', max_length=1000, null=True, blank=True)
    remarks = models.CharField(verbose_name='拜访备注', max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)

    class Meta:
        db_table = 'record'
        verbose_name = verbose_name_plural = "客户拜访记录"

    def __str__(self):
        return self.theme
