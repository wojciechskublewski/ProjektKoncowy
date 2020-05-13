from django.contrib.admin.widgets import AdminDateWidget

from .models import *
from django.forms import ModelForm, forms



class CIMAccountOpenForm(ModelForm):
    class Meta:
        model = CIMAccount
        fields = ['cim_number', 'lv_name', 'region', 'pm', 'eg_number', 'open_date','client_restrictions', 'special_templates']
        widgets = {'open_date' : AdminDateWidget}


class PMForm(ModelForm):
    class Meta:
        model = PM
        fields = '__all__'


class ChagesCreateForm(ModelForm):
    class Meta:
        model = Changes
        fields = '__all__'


class ChangesReviewMakerForm(ModelForm):
    class Meta:
        fields = ['']

