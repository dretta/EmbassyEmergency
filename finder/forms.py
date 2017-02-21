from django import forms

from .models import Country, Embassy

class CountryListForm(forms.Form):
    countries = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), 
		empty_label="Any String You Want None Option") #TODO: Figure out how to create None Option
		
class SubmitEmbed(forms.Form):
	url = forms.URLField()