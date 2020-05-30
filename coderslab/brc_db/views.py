from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, HttpResponse, redirect
from .forms import *
from .models import *
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views import View
from django.views.generic import TemplateView
from .functions import *
from django.contrib.auth import *
from django.core.mail import send_mail
from coderslab.settings import EMAIL_HOST_USER
import pandas as pd
from django.views.generic import RedirectView


# Create your views here.


class BaseView(LoginRequiredMixin, View):
    def get(self, request):
        form = CIMSearchForm
        pars = POSTReview.objects.filter(post_checked=False)[:10]
        ctx = {
            'form': form,
            'pars': pars
        }
        return render(request, 'base.html', ctx)

    def post(self, request):
        form = CIMSearchForm(request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            cim = form.cleaned_data['cim_number']
            return redirect(f'cim_details/{cim}')
        return render(request, 'base.html', ctx)


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
            return redirect('/changes_list/')
        return render(request, 'brc_db/change_form.html', ctx)


class ChangesReviewMakerListView(TemplateView):
    template_name = 'brc_db/changes_to_be_done_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['change'] = ChangesReview.objects.all().filter(change_checker_date=None)
        return ctx


class ChangesReviewMakerView(View):
    def get(self, request, pk):
        change = ChangesReview.objects.get(id=pk)
        form = ChangesReviewMakerForm
        ctx = {
            'form': form,
            'c': change
        }
        return render(request, 'brc_db/changes_maker_review.html', ctx)

    def post(self, request, pk):
        change = ChangesReview.objects.get(id=pk)
        if change.change_checker is not None:
            ctx = {'msg1': f'Change review is already done and checked!!!!'}
            return render(request, 'brc_db/changes_maker_review.html', ctx)
        form = ChangesReviewMakerForm(request.POST, instance=change)
        ctx = {
            'form': form,
            'c': change
        }
        if form.is_valid():
            form.save()
            change.change_maker_date = datetime.datetime.now().date()
            change.change_maker = request.user
            change.save()
            return redirect('/changes_list/')
        return render(request, 'brc_db/changes_maker_review.html', ctx)


class ChangesCheckerReviewView(PermissionRequiredMixin, View):
    permission_required = ('brc_db.can_validate',)

    def get(self, request, pk):
        change = ChangesReview.objects.get(id=pk)
        if change.change_checker is not None:
            ctx = {'msg1': 'Change is already done!!!'}
            return render(request, 'brc_db/changes_checker_review.html', ctx)
        form = ChangesReviewCheckerForm
        form1 = CheckerMailForm
        ctx = {
            'form': form,
            'c': change,
            'form1': form1
        }
        return render(request, 'brc_db/changes_checker_review.html', ctx)

    def post(self, request, pk):
        change = ChangesReview.objects.get(id=pk)
        form = ChangesReviewCheckerForm(request.POST, instance=change)
        form1 = CheckerMailForm(request.POST)
        ctx = {
            'form': form,
            'c': change,
            'form1': form1
        }
        if form.is_valid():
            if change.change_maker is None:
                ctx['msg'] = 'Review is not done by maker!!!'
                return render(request, 'brc_db/changes_checker_review.html', ctx)
            if change.change_maker == request.user:
                ctx['msg'] = 'Maker cannot be the same as checker!!!'
                return render(request, 'brc_db/changes_checker_review.html', ctx)
            form.save()
            change.change_checker = request.user
            change.change_checker_date = datetime.datetime.now().date()
            change.save()
            return redirect('/changes_list/')
        if form1.is_valid():
            mail_message = form1.cleaned_data['comment']
            mail_subject = f'Change review {change.cim_number} to be updated'
            send_mail(subject=mail_subject, message=mail_message,
                      from_email=EMAIL_HOST_USER, recipient_list=[change.change_maker.email], fail_silently=False)
            return redirect('/changes_list/')
        return render(request, 'brc_db/changes_checker_review.html', ctx)


class ClosedAccountUpdateView(UpdateView):
    model = CIMAccount
    template_name = 'brc_db/cimaccount_closing_update_form.html'
    fields = ['close_date', 'close_reason', 'closed']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cim'] = self.object.cim_number
        return context


class FundedAccountUpdateView(View):
    def get(self, request, pk):
        form = FundedCimForm
        cim = CIMAccount.objects.get(id=pk)
        return render(request, 'brc_db/cimaccount_funded_update_form.html', {'form': form, 'cim': cim})

    def post(self, request, pk):
        form = FundedCimForm(request.POST)
        cim = CIMAccount.objects.get(id=pk)
        if form.is_valid():
            c = form.instance
            cim.funded = c.funded
            cim.funded_date = c.funded_date
            cim.funded_amount = c.funded_amount
            cim.save()
            return redirect('/')
        return render(request, 'brc_db/cimaccount_funded_update_form.html', {'form': form, 'cim': cim})


class MakerPreChecklistView(View):
    def get(self, request, pk):
        pre = PREReview.objects.get(id=pk)
        if pre.pre_checker is not None:
            ctx = {
                'msg1': 'Pre review already done and checked!!!!'
            }
            return render(request,
                          'brc_db/pre_maker_checklist_update_form.html', ctx)
        form = PREMakerChecklistForm
        ctx = {
            'form': form,
            'pre': pre
        }
        return render(request,
                      'brc_db/pre_maker_checklist_update_form.html', ctx)

    def post(self, request, pk):
        form = PREMakerChecklistForm(request.POST)
        pre = PREReview.objects.get(id=pk)
        if form.is_valid():
            p = form.instance
            pre.ios_current = p.ios_current
            pre.ios_inline = p.ios_inline
            pre.ke_mp_mod = p.ke_mp_mod
            pre.ke_limited = p.ke_limited
            pre.cr_check = p.cr_check
            pre.sa_check = p.sa_check
            pre.fees_check = p.fees_check
            pre.pre_maker_date = datetime.datetime.now().date()
            pre.pre_maker = request.user
            pre.save()
            return redirect('/pre_review_list/')


class PreCheckerReviewView(View):
    def get(self, request, pk):
        pre = PREReview.objects.get(id=pk)

        if pre.pre_checker is not None:
            ctx = {
                'msg1': f'Checklist for CIM {pre.cim_number} is already done and checked!'
            }
            return render(request, 'brc_db/pre_checker_checklist_update_form.html', ctx)
        form = PreCheckerReviewForm
        form1 = CheckerMailForm
        ctx = {
            'form': form,
            'p': pre,
            'form1': form1
        }
        return render(request, 'brc_db/pre_checker_checklist_update_form.html', ctx)

    def post(self, request, pk):
        form = PreCheckerReviewForm(request.POST)
        form1 = CheckerMailForm(request.POST)
        pre = PREReview.objects.get(id=pk)
        ctx = {
            'form': form,
            'p': pre,
            'form1': form1
        }
        if form.is_valid():
            pre_post = form.instance
            if request.user == pre.pre_maker:
                ctx['msg'] = 'Maker cannot be the same as checker!!!!'
                return render(request, 'brc_db/pre_checker_checklist_update_form.html', ctx)
            if pre.pre_maker is None:
                ctx['msg'] = 'Not reviewed by maker'
                return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)
            pre.pre_checked = pre_post.pre_checked
            pre.pre_checker_date = datetime.datetime.now().date()
            pre.pre_checker = request.user
            pre.save()
            return redirect('/pre_review_list')
        if form1.is_valid():
            mail_message = form1.cleaned_data['comment']
            mail_subject = f'PRE Acceptance {pre.cim_number} to be updated'
            send_mail(subject=mail_subject, message=mail_message,
                      from_email=EMAIL_HOST_USER, recipient_list=[pre.pre_maker.email], fail_silently=False)
            return redirect('/pre_review_list/')

        return render(request, 'brc_db/pre_checker_checklist_update_form.html', ctx)


class POSTReviewNotDoneListView(TemplateView):
    template_name = 'brc_db/post_acceptance_to_be_done_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = POSTReview.objects.filter(cim_number__closed=False). \
            filter(post_checker_date__isnull=True).order_by('cim_number')
        ctx['post'] = post
        return ctx


class MakerPostChecklistView(View):
    def get(self, request, pk):
        p = POSTReview.objects.get(id=pk)
        if p.post_checker is not None:
            ctx = {
                'msg': f'Checklist for CIM {p.cim_number} is already done and checked!'
            }
            return render(request, 'brc_db/post_maker_checklist_update_form.html', ctx)
        c = CIMAccount.objects.get(cim_number=p.cim_number)
        form = PostMakerChecklistForm
        if not c.funded or c.funded_date is None or c.funded_amount is None:
            pk = c.id
            return redirect(f'/update_funded_CIM/{pk}/')
        return render(request, 'brc_db/post_maker_checklist_update_form.html',
                      {'form': form, 'cim': c})

    def post(self, request, pk):
        p = POSTReview.objects.get(id=pk)
        form = PostMakerChecklistForm(request.POST, instance=p)
        ctx = {'form': form}
        if form.is_valid():
            form.save()
            p.post_maker_date = datetime.datetime.now().date()
            p.maker = request.user
            p.save()
            return redirect('/post_list/')
        return render(request, 'brc_db/change_form.html', ctx)


class PostCheckerReviewView(View):
    def get(self, request, pk):
        p = POSTReview.objects.get(id=pk)
        if p.post_checker is not None:
            ctx = {
                'msg1': f'Checklist for CIM {p.cim_number} is already done and checked!'
            }
            return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)
        form = PostCheckerReviewForm
        form1 = CheckerMailForm
        ctx = {
            'form': form,
            'form1': form1,
            'p': p,
        }
        return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)

    def post(self, request, pk):
        form = PostCheckerReviewForm(request.POST)
        form1 = CheckerMailForm(request.POST)
        p = POSTReview.objects.get(id=pk)
        ctx = {
            'form': form,
            'form1': form1,
            'p': p,
        }
        if form.is_valid():
            p_post = form.instance
            if request.user == p.maker:
                ctx['msg'] = 'Maker cannot be the same as checker!!!!'
                return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)
            if p.maker is None:
                ctx['msg'] = 'Not reviewed by maker'
                return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)
            p.post_checked = p_post.post_checked
            p.post_checker_date = datetime.datetime.now().date()
            p.post_checker = request.user
            p.save()
            post_acc_checklist_pdf(pk)
            return redirect('/post_list')
        if form1.is_valid():
            mail_subject = f'PAR for {p.cim_number} rejected by Checker!'
            mail_message = form1.cleaned_data['comment']
            send_mail(p.maker.email, mail_subject, mail_message)
            return redirect('/post_list/')
        return render(request, 'brc_db/post_checker_checklist_update_form.html', ctx)


class LoginView(FormView):
    template_name = 'brc_db/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print("Zautentykowano, logowanie..", user)
            login(self.request, user)
            return redirect('/')
        else:
            ctx = {
                'msg': "Nie udało się zauntntykować",
                'form': LoginForm(self.request.POST)
            }
            return render(self.request, 'brc_db/login.html', ctx)


class CIMDetailsView(View):
    def get(self, request, cim):
        try:
            cim = CIMAccount.objects.get(cim_number=cim)
            ctx = {'cim': cim}
        except:
            return redirect('/')
        return render(request, 'brc_db/cim_details.html', ctx)


class PARDateQuery(View):
    def get(self, request):
        form = DateSearchForm
        ctx = {
            'form': form
        }
        return render(request, 'brc_db/par_date_search.html', ctx)

    def post(self, request):
        form = DateSearchForm(request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            pars = POSTReview.objects.filter(post_checker_date__gte=start_date, post_checker_date__lte=end_date)
            ctx = {
                'form': form,
                'pars': pars,
                'msg': 'wyniki zapytania',
                'start_date': start_date,
                'end_date': end_date
            }
            return render(request, 'brc_db/par_date_search.html', ctx)
        return render(request, 'brc_db/par_date_search.html', ctx)


class PARDateSearchToExcel(View):
    def get(self, request, start_date, end_date):
        try:
            panda_data = []
            pars = POSTReview.objects.filter(post_checker_date__gte=start_date,
                                             post_checker_date__lte=end_date)
            print(pars)
            for par in pars:
                list_pd = [par.cim_number.cim_number, par.post_maker_date, par.post_checker_date,
                           par.cim_number.funded_date, par.cim_number.funded_amount, par.maker, par.post_checker]
                panda_data.append(list_pd)

            panda_dada = pd.DataFrame(panda_data, columns=['CIM_number', 'Maker_date', 'Checker_date', 'Funded date',
                                                           'Funded_amount', 'Maker', 'Checker'])
            file_name = f'Par done {start_date} - {end_date}.csv'
            panda_dada.to_csv(file_name)
            return HttpResponse("File save on the share drive!")
        except:
            return HttpResponse("Please check input data!")


class CIMSearchView(View):
    def get(self, request):
        ctx = {
            'form_detail': CIMSearchForm,
            'form_update': CIMSearchFormUpdate,
        }
        return render(request, 'brc_db/search.html', ctx)

    def post(self, request):
        form_detail = CIMSearchForm(request.POST)
        form_update = CIMSearchFormUpdate(request.POST)
        ctx = {
            'form_detail': form_detail,
            'form_update': form_update,
        }
        if form_detail.is_valid():
            cim = form_detail.cleaned_data['cim_number']
            return redirect(f'/cim_details/{cim}')
        if form_update.is_valid():
            cim_number = form_update.cleaned_data['cim_update']
            cim = CIMAccount.objects.get(cim_number=cim_number)
            return redirect(f'/update_CIM/{cim.id}')
        return render(request, 'brc_db/search.html', ctx)


class LogoutAndRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return '/'
