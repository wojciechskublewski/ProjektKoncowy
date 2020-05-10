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


class OpenCIMView(View):
    def get(self, request):
        form = CIMAccountOpenForm()
        ctx = {'form': form}
        return render(request, 'brc_db/cimaccount_form.html', ctx)

    def post(self, request):
        form = CIMAccountOpenForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            cim = form.instance
            cim.save()
            p = PREReview()
            p.cim_number = cim
            p.save()
            return render(request, 'base.html')
        return request, 'brc_db/cimaccount_form.html', ctx


    # model = CIMAccount
    # success_url = '/'
    # #template_name = 'brc_db/cimaccount_form.html'
    # #form_class = CIMAccountOpenForm
    # fields = ['cim_number', 'lv_name', 'region', 'pm', 'eg_number', 'open_date', 'client_restrictions', 'special_templates']


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


class PREMakerView(CreateView):
    model = PREReview
    template_name = 'brc_db/pre_maker_review_form.html'
    fields = ['cim_number', 'ios_current', 'ios_inline']
    success_url = '/'


class PREREviewListView(TemplateView):
    template_name = 'brc_db/pre_list.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['cim'] = PREReview.objects.all().filter(pre_checker_date=None)
        return contex