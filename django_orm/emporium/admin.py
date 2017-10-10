from django.contrib import admin

from .models import Bargain, Supplier


class BargainAdmin(admin.ModelAdmin):
    list_display = ('description', 'price', 'sale_price', 'sku', 'supplier')

admin.site.register(Bargain, BargainAdmin)
admin.site.register(Supplier)
