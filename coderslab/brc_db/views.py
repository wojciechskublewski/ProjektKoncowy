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
            c = form.instance
            # c = CIMAccount()
            # c.cim_number = form.cleaned_data['cim_number']
            # c.lv = form.cleaned_data['lv_name']
            # c.region = form.cleaned_data['region']
            # c.pm = form.cleaned_data['pm']
            # c.eg_number = form.cleaned_data['eg_number']
            # c.client_restrictions = form.cleaned_data['client_restrictions']
            # c.special_templates = form.cleaned_data['special_templates']
            c.save()
            pre = PREReview()
            pre.cim_number = c
            pre.save()
            post = POSTReview()
            post.cim_number = c
            post.save()
            return render(request, 'base.html')
        return render(request, 'brc_db/cimaccount_form.html', ctx)


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
        ctx = super().get_context_data(**kwargs)
        ctx['cim'] = PREReview.objects.all().filter(pre_checker_date=None)
        return ctx


class LVCreateView(CreateView):
    model = LV
    success_url = '/'
    fields = '__all__'
    template_name = 'brc_db/lv_form.html'


class RegionCreatView(CreateView):
    model = Region
    success_url = '/'
    fields = '__all__'
    template_name = 'brc_db/region_form.html'


class ChangesCreateView(View):
    def get(self, request):
        form = ChagesCreateForm
        ctx = {'form': form}
        return render(request, 'brc_db/change_form.html', ctx)

    def post(self, request):
        form = ChagesCreateForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            c = form.instance
            c.save()
            c_review = ChangesReview()
            c_review.cim_number = c.cim_number
            c_review.change = c
            c_review.save()
            return render(request, 'base.html')
        return render(request, 'brc_db/change_form.html', ctx)


class ChangesReviewMakerListView(TemplateView):
    template_name = 'brc_db/changes_to_be_done_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['change'] = ChangesReview.objects.all().filter(change_checker_date=None)
        return ctx

