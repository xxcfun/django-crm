from django.db import models

# Create your models here.
from utils import constants


class User(models.Model):
    """用户表"""
    name = models.CharField(verbose_name='用户名', max_length=128, unique=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    professional = models.CharField(verbose_name='职称', max_length=64, null=True, blank=True)
    role = models.SmallIntegerField(verbose_name='权限', choices=constants.USER_ROLE, default=constants.ROLE_YW)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_time']
        verbose_name_plural = verbose_name = '用户'

    def __str__(self):
        return self.name


class Count(models.Model):
    """用户数据统计"""
    user_id = models.IntegerField(verbose_name='用户id', primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=64, null=True, blank=True)
    day_customer = models.IntegerField(verbose_name='今天新增客户数量', default=0)
    day_liaison = models.IntegerField(verbose_name='今天新增联系人数量', default=0)
    day_record = models.IntegerField(verbose_name='昨天拜访记录数量', default=0)
    day_business = models.IntegerField(verbose_name='今天新增商机数量', default=0)

    month_customer = models.IntegerField(verbose_name='本月新增客户数量', default=0)
    month_liaison = models.IntegerField(verbose_name='本月新增联系人数量', default=0)
    month_record = models.IntegerField(verbose_name='本月新增拜访记录数量', default=0)
    month_business = models.IntegerField(verbose_name='本月新增商机数量', default=0)

    all_customer = models.IntegerField(verbose_name='全部客户数量', default=0)
    all_liaison = models.IntegerField(verbose_name='全部联系人数量', default=0)
    all_record = models.IntegerField(verbose_name='全部拜访记录数量', default=0)
    all_business = models.IntegerField(verbose_name='全部商机数量', default=0)

    class Meta:
        db_table = 'count'
        verbose_name = verbose_name_plural = "用户数据统计"

    def __str__(self):
        return self.name


class Date(models.Model):
    """日期表"""
    day = models.IntegerField(verbose_name='日期')
    month = models.IntegerField(verbose_name='月份')

    class Meta:
        db_table = 'date'
        verbose_name_plural = verbose_name = '日期表'

    def __str__(self):
        return self.day
