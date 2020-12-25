from django.forms import ModelForm

from record.models import Record


class RecordForm(ModelForm):
    """联系人表单"""
    class Meta:
        model = Record
        exclude = ['is_valid', 'created_at', 'updated_at']
