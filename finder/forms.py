from django import forms

from .models import Country, Embassy

class CountryListForm(forms.Form):
    countries = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), 
		empty_label="Any String You Want None Option") #TODO: Figure out how to create None Option
		
class CountryUpdateForm(forms.Form):
	country = forms.CharField(label='Country Name', max_length=50)

class EmbassyUpdateForm(forms.form):
	pass
	
