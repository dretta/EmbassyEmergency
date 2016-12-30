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
    return HttpResponse("You're looking at the Embassy %s." % embassy_id)

def country_info(request, code):
    response = "You're looking at the Country %s."
    return HttpResponse(response % code)

def results(request, government_code, location_code):
	print(government_code, location_code)
	government = Country.objects.get(code=government_code)
	location = Country.objects.get(code=location_code)
	return HttpResponse("Here are the Embassies sent by %s, located in %s." % (government.name, location.name))
	
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
			# return HttpResponseRedirect(reverse('finder:results', kwargs={'government':goverment.code, 'location':location.code}))
