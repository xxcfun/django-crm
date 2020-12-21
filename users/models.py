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
