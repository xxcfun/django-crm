from django.forms import ModelForm

from business.models import Business


class BusinessForm(ModelForm):
    """联系人表单"""
    class Meta:
        model = Business
        exclude = ['is_valid', 'created_at', 'updated_at']
