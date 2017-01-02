from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Country, Embassy
from django.template import loader
from django.urls import reverse
from django.views import generic

class IndexView(generic.base.TemplateView):
    template_name = "finder/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context
	
class EmbassyView(generic.DetailView):
    model = Embassy
    template_name = 'finder/embassy_info.html'

class CountryView(generic.DetailView):
    model = Country
    template_name = 'finder/country_info.html'

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
