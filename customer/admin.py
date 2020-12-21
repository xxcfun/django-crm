from django.contrib import admin

# Register your models here.
from customer.models import Customer, CustomerShop, CustomerInvoice


"""客户信息"""
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'website', 'scale', 'nature', 'industry',
                    'remarks', 'user', 'is_valid')
    list_per_page = 10


"""客户收货地址信息"""
@admin.register(CustomerShop)
class CustomerShopAdmin(admin.ModelAdmin):
    list_display = ('customer', 'shop_province', 'shop_city', 'shop_area',
                    'shop_address', 'shop_username', 'shop_phone')
    list_per_page = 10


"""客户发票地址信息"""
@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'invoice_province', 'invoice_city', 'invoice_area',
                    'invoice_address', 'invoice_username', 'invoice_phone')
    list_per_page = 10
