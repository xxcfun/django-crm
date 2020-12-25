from django.forms import ModelForm

from liaison.models import Liaison


class LiaisonForm(ModelForm):
    """联系人表单"""
    class Meta:
        model = Liaison
        exclude = ['is_valid', 'created_at', 'updated_at']
