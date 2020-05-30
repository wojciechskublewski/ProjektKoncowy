from django.contrib.admin.widgets import AdminDateWidget

from .models import *
from django.forms import ModelForm, forms, widgets
from django import forms



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
        fields = ['ios_current', 'ios_inline', 'ke_mp_mod', 'ke_limited',
                  'fees_check', 'cr_check', 'sa_check', 'comment']


class PostMakerChecklistForm(ModelForm):
    class Meta:
        model = POSTReview
        fields = ['fees_checked', 'letter_sent', 'cr_client_restriction', 'cr_aa_bg_system', 'cr_sa', 'comment']


class FundedCimForm(ModelForm):
    class Meta:
        model = CIMAccount
        fields = ['funded', 'funded_date', 'funded_amount']


class PostCheckerReviewForm(ModelForm):
    class Meta:
        model = POSTReview
        fields = ['post_checked']

    def clean(self):
        cleaned_data = super().clean()
        checked = cleaned_data.get('post_checked')
        print(checked)
        if checked is None or checked is False:
            raise forms.ValidationError('Potwierdz ze sprawdziles wszystkie zmiany!')


class PreCheckerReviewForm(ModelForm):
    class Meta:
        model = PREReview
        fields = ['pre_checked']

    def clean(self):
        cleaned_data = super().clean()
        checked = cleaned_data.get('pre_checked')
        print(checked)
        if checked is None or checked is False:
            raise forms.ValidationError('Potwierdz ze sprawdziles wszystkie zmiany!')


class ChangesReviewMakerForm(ModelForm):
    class Meta:
        model = ChangesReview
        fields = ['fees_checked', 'cr_client_restriction', 'cr_aa_br_system',
                  'cr_sa', 'ke_knowledge', 'comment']


class ChangesReviewCheckerForm(ModelForm):
    class Meta:
        model = ChangesReview
        fields = ['change_checked']

    def clean(self):
        cleaned_data = super().clean()
        checked = cleaned_data.get('change_checked')
        print(checked)
        if checked is None or checked is False:
            raise forms.ValidationError('Potwierdz ze sprawdziles wszystkie zmiany!')


class LoginForm(forms.Form):
    login = forms.CharField(label="login", max_length=64)
    password = forms.CharField(label="password", max_length=64, widget=forms.PasswordInput)


class CIMSearchForm(forms.Form):
    cim_number = forms.CharField(label='cim_number', max_length=4)


class CheckerMailForm(forms.Form):
    comment = forms.CharField(label="Comment to maker", widget=forms.Textarea)


class DateSearchForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError('start date nie moze byc wieksza niz end date')


class CIMSearchFormUpdate(forms.Form):
    cim_update = forms.CharField(label='cim_update', max_length=4)


