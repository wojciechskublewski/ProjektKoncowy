from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import ForeignKey

CHECKLIST_VALUES = (
    (1, "N/A"),
    (2, "N"),
    (3, "y"),
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
    cim_number = models.CharField(max_length=4, unique=True)
    lv_name = models.ForeignKey(LV, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    pm = models.ForeignKey(PM, on_delete=models.CASCADE)
    eg_number = models.CharField(max_length=16)
    open_date = models.DateField()
    close_date = models.DateField(null=True, blank=True)
    close_reason = models.CharField(max_length=128, null=True, blank=True)
    client_restrictions = models.TextField(null=True, blank=True)
    special_templates = models.ManyToManyField(SpecialRestriction, default=None, blank=True)
    funded = models.BooleanField(null=True, blank=True)


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
    pre_maker_date = models.DateField(null=True, blank=True)
    pre_maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='pre_maker', blank=True)
    pre_checker_date = models.DateField(null=True, blank=True)
    pre_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='pre_checker', blank=True)


class POSTReview(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    fees_checked = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    letter_sent = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_client_restriction = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_aa_bg_system = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_sa = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    post_maker_date = models.DateField(null=True, blank=True)
    maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='post_maker', blank=True)
    post_checker_date = models.DateField(null=True, blank=True)
    post_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='post_checker', blank=True)


class Changes(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    change_date = models.DateField()
    change_name = models.IntegerField(choices=CHANGES)


class ChangesReview(models.Model):
    cim_number = models.ForeignKey(CIMAccount, on_delete=models.CASCADE)
    change = models.ForeignKey(Changes, on_delete=models.CASCADE)
    fees_checked = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_client_restriction = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_aa_br_system = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    cr_sa = models.IntegerField(choices=CHECKLIST_VALUES, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    change_maker_date = models.DateField(null=True, blank=True)
    change_maker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='change_maker', blank=True)
    change_checker_date = models.DateField(null=True, blank=True)
    change_checker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='change_checker', blank=True)

