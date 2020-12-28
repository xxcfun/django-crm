
from django.db import models

# Create your models here.
from users.models import User
from utils import constants


class Customer(models.Model):
    """客户模型"""
    name = models.CharField(verbose_name='客户名称', max_length=64, unique=True)
    rank = models.SmallIntegerField(verbose_name='客户级别', choices=constants.CUSTOMER_RANK, default=constants.RANK_NORMAL)
    website = models.CharField(verbose_name='客户网址', max_length=255, blank=True, null=True)
    scale = models.SmallIntegerField(verbose_name='客户规模', choices=constants.CUSTOMER_SCALE, default=constants.SCALE_TEN, null=True, blank=True)
    nature = models.SmallIntegerField(verbose_name='客户性质', choices=constants.CUSTOMER_NATURE, default=constants.NATURE_YX, null=True, blank=True)
    industry = models.SmallIntegerField(verbose_name='客户行业', choices=constants.CUSTOMER_INDUSTRY, default=constants.INDUSTRY_JTSB, null=True, blank=True)
    remarks = models.CharField(verbose_name='客户备注', max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='创建人', related_name='customer', on_delete=models.CASCADE)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'customer'
        verbose_name = verbose_name_plural = "客户"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CustomerShop(models.Model):
    """客户收货地址信息"""
    customer = models.OneToOneField(Customer, verbose_name='客户名称', related_name='customer_shop', on_delete=models.CASCADE)
    shop_province = models.CharField(verbose_name='收货省份', max_length=32, blank=True, null=True)
    shop_city = models.CharField(verbose_name='收货市区', max_length=32, blank=True, null=True)
    shop_area = models.CharField(verbose_name='收货区域', max_length=32, blank=True, null=True)
    shop_town = models.CharField(verbose_name='收货街道', max_length=32, blank=True, null=True)
    shop_address = models.CharField(verbose_name='收货详细地址', max_length=64, blank=True, null=True)
    shop_username = models.CharField(verbose_name='收货地收货人', max_length=32, blank=True, null=True)
    shop_phone = models.CharField(verbose_name='收货收货人电话', max_length=32, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def shop_address_add(self, pk):
        self.customer_id = pk
        self.save()
        self.refresh_from_db()

    class Meta:
        db_table = 'customer_shop'
        verbose_name = verbose_name_plural = "客户收货地址信息"
        ordering = ['-created_at']

    def __str__(self):
        return self.customer.name


class CustomerInvoice(models.Model):
    """客户发票地址信息"""
    customer = models.OneToOneField(Customer, verbose_name='客户名称', related_name='customer_invoice', on_delete=models.CASCADE)
    invoice_province = models.CharField(verbose_name='发票省份', max_length=32, blank=True, null=True)
    invoice_city = models.CharField(verbose_name='发票市区', max_length=32, blank=True, null=True)
    invoice_area = models.CharField(verbose_name='发票区域', max_length=32, blank=True, null=True)
    invoice_town = models.CharField(verbose_name='发票街道', max_length=32, blank=True, null=True)
    invoice_address = models.CharField(verbose_name='发票详细地址', max_length=64, blank=True, null=True)
    invoice_username = models.CharField(verbose_name='发票地收货人', max_length=32, blank=True, null=True)
    invoice_phone = models.CharField(verbose_name='发票收货人电话', max_length=32, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'customer_invoice'
        verbose_name = verbose_name_plural = "客户发票地址信息"
        ordering = ['-created_at']

    def __str__(self):
        return self.customer.name
