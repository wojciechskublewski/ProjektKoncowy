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


class PREMakerChecklistForm(ModelForm):
    class Meta:
        model = PREReview
        fields = ['ios_current', 'ios_inline', 'ke_mp_mod', 'ke_limited', 'fees_check', 'cr_check', 'sa_check']


