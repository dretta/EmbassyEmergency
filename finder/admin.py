from django.contrib import admin

from .models import Country, Embassy

class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'code']
	
class EmbassyAdmin(admin.ModelAdmin):
    fields = ['name', 'government', 'location', 'street_address', 'city', 'phone_number', 'fax_number', 'email_address', 'website']

admin.site.register(Country, CountryAdmin)
admin.site.register(Embassy, EmbassyAdmin)
