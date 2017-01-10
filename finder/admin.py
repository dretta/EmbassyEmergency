from django.contrib import admin

from .models import Country, Embassy

class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'code']

admin.site.register(Country, CountryAdmin)
admin.site.register(Embassy)
