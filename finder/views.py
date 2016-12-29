from django.shortcuts import render

from django.http import HttpResponse


def index(request):
	return HttpResponse("Find your Embassy:")
	
def embassy_info(request, embassy_id):
    return HttpResponse("You're looking at the Embassy %s." % embassy_id)

def country_info(request, code):
    response = "You're looking at the Country %s."
    return HttpResponse(response % code)

def results(request, government, location):
    return HttpResponse("Here are the Embassies sent by %s, located in %s." % (government, location))
