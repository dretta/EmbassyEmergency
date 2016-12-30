from django import forms

from .models import Country, Embassy

class CountryListForm(forms.Form):
    countries = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'))