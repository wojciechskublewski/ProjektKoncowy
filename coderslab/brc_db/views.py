from django.shortcuts import render, HttpResponse
from .forms import *
from .models import *
from django.views.generic.edit import  FormView, CreateView, UpdateView
from django.views import View
from django.views.generic import TemplateView

# Create your views here.


class BaseView(View):
    def get(self, request):
        return render(request, 'base.html')


class OpenCIMView(CreateView):
    model = CIMAccount
    success_url = '/'
    #template_name = 'brc_db/cimaccount_form.html'
    #form_class = CIMAccountOpenForm
    fields = ['cim_number', 'lv_name', 'region', 'pm', 'eg_number', 'open_date', 'client_restrictions', 'special_templates']


class PMCreateView(CreateView):
    model = PM
    success_url = '/'
    fields = '__all__'


class SpecialRestrictionCreateView(CreateView):
    model = SpecialRestriction
    success_url = '/'
    fields = '__all__'


class UpdateCIMView(UpdateView):
    model = CIMAccount
    template_name = 'brc_db/cimaccount_update_form.html'
    fields = ['lv_name', 'region', 'pm', 'eg_number', 'open_date', 'client_restrictions', 'special_templates']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cim'] = self.object.cim_number
        return context


