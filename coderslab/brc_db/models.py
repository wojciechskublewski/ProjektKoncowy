from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.db.models import ForeignKey

CHECKLIST_VALUES = (
    (1, "N/A"),
    (2, "N"),
    (3, "Y"),
)


CHANGES = (
    (1, "BM change"),
    (2, "Product change"),
    (3, "Level change"),
    (4, "Fee change"),
)


class PM(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.name


class LV(models.Model):
    lv_name = models.CharField(max_length=20)

    @property
    def name(self):
        return f'{self.lv_name}'

    def __str__(self):
        return self.name


class Region(models.Model):
    region_name = models.CharField(max_length=20)

    @property
    def name(self):
        return f'{self.region_name}'

    def __str__(self):
        return self.name


class SpecialRestriction(models.Model):
    template_rule_name = models.CharField(max_length=128, unique=True)


    @property
    def name(self):
        return f'{self.template_rule_name}'


    def __str__(self):
        return self.name


class CIMAccount(models.Model):
    cim_number = models.CharField(max_length=4, unique=True, verbose_name='CIM')
    lv_name = models.ForeignKey(LV, on_delete=models.CASCADE, verbose_name='LV')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region')
    pm = models.ForeignKey(PM, on_delete=models.CASCADE, verbose_name='PM')
    eg_number = models.CharField(max_length=16, verbose_name='EG')
    open_date = models.DateField(verbose_name='Open Date')
    close_date = models.DateField(null=True, blank=True, verbose_name='Close date')
    close_reason = models.CharField(max_length=128, null=True, blank=True, verbose_name='Reason of closing')
    closed = models.BooleanField(default=False, verbose_name='Closed')
    client_restrictions = models.TextField(null=True, blank=True, verbose_name='Client restrictions')
    special_templates = models.ManyToManyField(SpecialRestriction, default=None, blank=True,
                                               verbose_name='Special rules')
    funded = models.BooleanField(null=True, blank=True, verbose_name='Funded')
    funded_date = models.DateField(blank=True, null=True, verbose_name='Funded date')
    funded_amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=12,
                                        verbose_name='Funded amount')


    @property
    def name(self):
        return f'{self.cim_number}'

    def __str__(self):
        return self.name


class PREReview(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    ios_current = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    ios_inline = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    ke_mp_mod = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    ke_limited = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    fees_check = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_check = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    sa_check = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    pre_checked = models.BooleanField(default=False)
    pre_maker_date = models.DateField(null=True, blank=True)
    pre_maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='pre_maker', blank=True)
    pre_checker_date = models.DateField(null=True, blank=True)
    pre_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='pre_checker', blank=True)


class POSTReview(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE,)
    fees_checked = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True,
                                       verbose_name='Fess checked and in line?')
    letter_sent = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True,
                                      verbose_name='Is client restriction letter sent?')
    cr_client_restriction = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True,
                                                verbose_name='Are client restrictions incldued in Charles River?')
    cr_aa_bg_system = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True,
                                          verbose_name='Are asset allocation / business rules / cim system included in Charles River')
    cr_sa = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True,
                                verbose_name='Substantial affiliation included in Charles River?')
    comment = models.TextField(blank=True, null=True)
    post_maker_date = models.DateField(null=True, blank=True)
    maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='post_maker', blank=True)
    post_checked = models.BooleanField(default=False)
    post_checker_date = models.DateField(null=True, blank=True)
    post_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='post_checker', blank=True)

    @property
    def number_post_days(self):
        if self.cim_number.funded:
            return (datetime.datetime.now().date() - self.cim_number.funded_date).days
        else:
            return (datetime.datetime.now().date() - self.cim_number.open_date).days

    @property
    def number_days_checked(self):
        return (self.post_checker_date - self.cim_number.funded_date).days


class Changes(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    change_date = models.DateField()
    change_name = models.IntegerField(choices=CHANGES)


class ChangesReview(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    change = models.ForeignKey(Changes, on_delete=models.CASCADE)
    fees_checked = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    ke_knowledge = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_client_restriction = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_aa_br_system = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_sa = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    change_checked = models.BooleanField(default=False)
    change_maker_date = models.DateField(null=True, blank=True)
    change_maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='change_maker', blank=True)
    change_checker_date = models.DateField(null=True, blank=True)
    change_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                       related_name='change_checker', blank=True)

    class Meta:
        permissions = (
            ('can_review', 'Maker review'),
            ('can_validate', 'Checker review')
        )

