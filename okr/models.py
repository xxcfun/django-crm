from django.db import models

# Create your models here.
from users.models import User
from utils import constants


class Okr(models.Model):
    """okr个人目标"""
    object = models.CharField(verbose_name='目标', max_length=255)
    key1 = models.CharField(verbose_name='关键成果1', max_length=255, null=True, blank=True)
    key1_true = models.SmallIntegerField(verbose_name='完成情况1', choices=constants.OKR_FINISH, null=True, blank=True)
    key2 = models.CharField(verbose_name='关键成果2', max_length=255, null=True, blank=True)
    key2_true = models.SmallIntegerField(verbose_name='完成情况2', choices=constants.OKR_FINISH, null=True, blank=True)
    key3 = models.CharField(verbose_name='关键成果3', max_length=255, null=True, blank=True)
    key3_true = models.SmallIntegerField(verbose_name='完成情况3', choices=constants.OKR_FINISH, null=True, blank=True)
    results = models.CharField(verbose_name='衡量标准', max_length=255, null=True, blank=True)
    finish = models.CharField(verbose_name='实际达成', max_length=255, null=True, blank=True)

    user = models.ForeignKey(User, verbose_name='创建人', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)

    class Meta:
        db_table = 'okr'
        verbose_name = verbose_name_plural = 'okr'
        ordering = ['-created_at']

    def __str__(self):
        return self.object
