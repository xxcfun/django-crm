from django.forms import ModelForm

from okr.models import Okr


class OkrForm(ModelForm):
    """okr表单"""
    class Meta:
        model = Okr
        exclude = ['is_valid', 'created_at', 'updated_at']
