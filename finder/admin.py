from django.contrib import admin

from .models import Country, Embassy

class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'code']
	
class EmbassyAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               	{'fields': ['name', 'government', 'location']}),
		('Contact information', {'fields': ['street_address', 'city', 'phone_number', 'fax_number', 'email_address', 'website']}),
	]
	search_fields = ['name']

admin.site.register(Country, CountryAdmin)
admin.site.register(Embassy, EmbassyAdmin)
