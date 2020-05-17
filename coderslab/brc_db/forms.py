from django.contrib.admin.widgets import AdminDateWidget

from .models import *
from django.forms import ModelForm, forms, widgets



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


class PostMakerChecklistForm(ModelForm):
    class Meta:
        model = POSTReview
        fields = ['fees_checked', 'letter_sent', 'cr_client_restriction', 'cr_aa_bg_system', 'cr_sa']


class FundedCimForm(ModelForm):
    class Meta:
        model = CIMAccount
        fields = ['funded', 'funded_date', 'funded_amount']


class PostCheckerReviewForm(ModelForm):
    class Meta:
        model = POSTReview
        fields = ['post_checked']



