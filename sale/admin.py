from django.contrib import admin

# Register your models here.

from sale.models import *


class SaleInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_per_page = 10


admin.site.register(SaleInfo, SaleInfoAdmin)


class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ("title", 'price', 'num', 'status')
    list_per_page = 10


admin.site.register(Specifications, SpecificationsAdmin)
