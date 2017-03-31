from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Country, Embassy
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
import requests
from .forms import BootstrapModelForm
from django.forms import modelform_factory

class IndexView(generic.base.TemplateView):
	template_name = "finder/index.html"

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['countries'] = Country.objects.all()
		return context
		
class EmbassyListView(generic.ListView):
	model = Embassy
	template_name = "finder/embassy_list.html"
	
class CountryListView(generic.ListView):
	model = Country
	template_name = "finder/country_list.html"
	
class EmbassyCreateView(generic.edit.CreateView):
	model = Embassy
	fields = ['government','location','name','street_address','city','phone_number','fax_number','email_address','website']
	template_name_suffix = '_create'
	
	def post(self, request, *args, **kwargs):
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse('finder:embassy_list'))
		else:
			#autoUpdate defaults to True, although manually made Embassies should have it as False
			post = request.POST.copy()
			post['autoUpdate'] = False
			request.POST = post
			return super(EmbassyCreateView, self).post(request, *args, **kwargs)

class CountryCreateView(generic.edit.CreateView):
	model = Country
	fields = ['code', 'name']
	template_name_suffix = '_create'
	
	def post(self, request, *args, **kwargs):
		if "cancel" in request.POST:
			return HttpResponseRedirect(reverse('finder:country_list'))
		else:
			return super(CountryCreateView, self).post(request, *args, **kwargs)

class EmbassyEditView(generic.edit.UpdateView):
	model = Embassy
	fields = ['name', 'street_address', 'city', 'phone_number', 'fax_number', 'email_address', 'website']
	template_name_suffix = '_edit'
	
	def get_form_class(self):
		return modelform_factory(self.model, form=BootstrapModelForm, fields=self.fields)
	
	def post(self, request, *args, **kwargs):
		print(self)
		if "cancel" in request.POST:
			object = self.get_object()
			return redirect(object)
		else:
			return super(EmbassyEditView, self).post(request, *args, **kwargs)

class CountryEditView(generic.edit.UpdateView):
	model = Country
	fields = ['name']
	template_name_suffix = '_edit'	
	
	def get_form_class(self):
		return modelform_factory(self.model, form=BootstrapModelForm, fields=self.fields)
	
	def post(self, request, *args, **kwargs):
		print(self)
		if "cancel" in request.POST:
			object = self.get_object()
			return redirect(object)
		else:
			return super(CountryEditView, self).post(request, *args, **kwargs)

class EmbassyDeleteView(generic.edit.DeleteView):
	model = Embassy
	template_name_suffix = '_delete'
	success_url = reverse_lazy('finder:embassy_list')
	
	def post(self, request, *args, **kwargs):
		print(self)
		if "cancel" in request.POST:
			object = self.get_object()
			return redirect(object)
		else:
			return super(EmbassyDeleteView, self).post(request, *args, **kwargs)
			
class CountryDeleteView(generic.edit.DeleteView):
	model = Country
	template_name_suffix = '_delete'
	success_url = reverse_lazy('finder:country_list')
	
	def post(self, request, *args, **kwargs):
		print(self)
		if "cancel" in request.POST:
			object = self.get_object()
			return redirect(object)
		else:
			return super(CountryDeleteView, self).post(request, *args, **kwargs)
			
	def get_context_data(self, **kwargs):
		context = super(CountryDeleteView, self).get_context_data(**kwargs)
		context['hasEmbassy'] = Embassy.objects.select_related().filter(government=self.get_object().code).exists() or 
			Embassy.objects.select_related().filter(location=self.get_object().code).exists()
		return context
			
class EmbassyView(generic.DetailView):
	model = Embassy
	template_name = 'finder/embassy_info.html'

class CountryView(generic.DetailView):
	model = Country
	template_name = 'finder/country_info.html'
	
	def get_context_data(self, **kwargs):
		context = super(CountryView, self).get_context_data(**kwargs)
		context['governments'] = Embassy.objects.select_related().filter(government=self.get_object().code)
		context['locations'] = Embassy.objects.select_related().filter(location=self.get_object().code)
		return context
		
class AboutView(generic.base.TemplateView):
	template_name = "finder/about.html"
	
class ContactView(generic.base.TemplateView):
	template_name = "finder/contact.html"

def results(request, government_code, location_code):
	government = Country.objects.get(code=government_code)
	location = Country.objects.get(code=location_code)
	embassy = Embassy.objects.filter(government=government_code, location=location_code)
	context = {'embassies':embassy, 'government':government, 'location':location}
	return render(request, 'finder/results.html', context)
	
def search(request):
	countries  = Country.objects.all()
	form = request.POST
	if request.method == 'POST':
		try:
			selected_government = get_object_or_404(Country, pk=request.POST['government'])
		except (KeyError, Country.DoesNotExist):
			# Redisplay the country selection forms.
			return render(request, 'finder/index.html', {
				'error_message': "You didn't select a government.",
			})
		try:
			selected_location = get_object_or_404(Country, pk=request.POST['location'])
		except (KeyError, Country.DoesNotExist):
			# Redisplay the country selection forms.
			return render(request, 'finder/index.html', {
				'error_message': "You didn't select a location.",
			})
		else:
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('finder:results', args=(selected_government.code,selected_location.code,)))
