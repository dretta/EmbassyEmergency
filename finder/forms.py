from django import forms

from .models import Country, Embassy

class CountryListForm(forms.Form):
    countries = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), 
		empty_label="Any String You Want None Option") #TODO: Figure out how to create None Option
		
class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })