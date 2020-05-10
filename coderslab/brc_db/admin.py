from django.contrib import admin
from brc_db.models import Region, LV, PM, CIMAccount

# Register your models here.

admin.site.register(Region)
admin.site.register(LV)
admin.site.register(PM)
admin.site.register(CIMAccount)