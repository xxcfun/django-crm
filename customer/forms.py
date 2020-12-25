from django.forms import ModelForm

from customer.models import Customer, CustomerShop, CustomerInvoice


class CustomerForm(ModelForm):
    """客户表单"""
    class Meta:
        model = Customer
        fields = ('name', 'rank', 'website', 'scale', 'nature', 'industry', 'remarks', 'user')


class CustomerShopForm(ModelForm):
    class Meta:
        model = CustomerShop
        exclude = ['created_at', 'updated_at']


class CustomerInvoiceForm(ModelForm):
    class Meta:
        model = CustomerInvoice
        exclude = ['created_at', 'updated_at']