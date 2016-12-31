from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Country, Embassy
from django.template import loader
from django.urls import reverse


def index(request):
	country = Country.objects.filter()
	template = loader.get_template('finder/index.html')
	context = {'countries': country}
	return render(request, 'finder/index.html', context)
	
def embassy_info(request, embassy_id):
	embassy = get_object_or_404(Embassy, pk=embassy_id)
	context = {'embassy': embassy}
	return render(request, 'finder/embassy_info.html', context)

def country_info(request, code):
	country = get_object_or_404(Country, code=code)
	context = {'country': country}
	return render(request, 'finder/country_info.html', context)

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
