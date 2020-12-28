from django.db import models

from customer.models import Customer
from users.models import User
from utils import constants


class Liaison(models.Model):
    """联系人模型"""
    customer = models.ForeignKey(Customer, verbose_name='客户', related_name='liaison', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='联系人姓名', max_length=64)
    phone = models.CharField(verbose_name='联系人电话', max_length=11)
    job = models.SmallIntegerField(verbose_name='职称', choices=constants.LIAISON_JOB, default=constants.JOB_BUSINESS)
    injob = models.SmallIntegerField(verbose_name='是否在职', choices=constants.LIAISON_INJOB, default=constants.INJOB_YES)
    wx = models.CharField(verbose_name='微信', max_length=64, blank=True, null=True)
    qq = models.CharField(verbose_name='QQ', max_length=64, blank=True, null=True)
    email = models.EmailField(verbose_name='电子邮箱', max_length=64, blank=True, null=True)
    hobby = models.CharField(verbose_name='兴趣爱好', max_length=128, blank=True, null=True)
    birthday = models.CharField(verbose_name='生日', max_length=64, blank=True, null=True)
    remarks = models.CharField(verbose_name='联系人备注', max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='创建人', related_name='liaison', on_delete=models.CASCADE)

    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'liaison'
        verbose_name = verbose_name_plural = "联系人"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
