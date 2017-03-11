import overpy
import json
import time
from .models import Country, Embassy
import requests
import xml.etree.ElementTree 




def runQuery(): 
	api = overpy.Overpass()
	api.max_retry_count = 3
	# fetch all ways and nodes
	result = api.query("""
[out:json];
(
	(
		( 
			node[amenity=embassy][country][target]["addr:street"]["addr:city"]["contact:phone"]; 
				- node[amenity=embassy][diplomatic][diplomatic!=embassy]; 
		);
			- node[amenity=embassy][!name][!"name:en"];
	);
	( 
		(
			way[amenity=embassy][country][target]["addr:street"]["addr:city"]["contact:phone"];  
				- way[amenity=embassy][diplomatic][diplomatic!=embassy]; 
		);
			- way[amenity=embassy][!name][!"name:en"];
	);
	( 
		(
			rel[amenity=embassy][country][target]["addr:street"]["addr:city"]["contact:phone"];  
				- rel[amenity=embassy][diplomatic][diplomatic!=embassy]; 
		);
			- rel[amenity=embassy][!name][!"name:en"];
	);
);
out tags;  
		""")

	
		
	
	return result
	
def queryAttempts(attempts=100):
	while attempts > 0:
		try:
			queryResult = runQuery()
			break
		except overpy.exception.OverpassTooManyRequests as e:
			time.sleep(60)
		except json.decoder.JSONDecodeError as e: 
			attempts -= 1
			print("Query failed, {} number of attempt(s) left".format(attempts))
			time.sleep(60)
		except overpy.exception.OverpassGatewayTimeout:
			print("Server is over-loaded, will not update database")
			return None
		except overpy.exception.OverpassUnknownHTTPStatusCode:
			print("Unknown Overpy Error, will not update database")
			return None
			
			
	if attempts == 0:
		raise e
	else:
		return queryResult
		
def canUpdate(government, location):
	try:
		governmentObj = getCountryObj(government)
		locationObj = getCountryObj(location)
	except requests.RequestException as e:
		raise e
	else:
		assert governmentObj 
		assert locationObj
	
	if Embassy.objects.filter(government=governmentObj,location=locationObj).exists():
		return False # There shouldn't be multiple embassies with the same government and location, for now...
	else:
		return (governmentObj, locationObj)
	
def getCountryObj(country):
	try:
		countryObj = Country.objects.get(pk=country) # Only gets a country if it's not auto updated
	except Country.DoesNotExist: # Otherwise use the World Bank API to get a fresh/new one
		resp = requests.get('http://api.worldbank.org/countries/{}'.format(country))
		root = xml.etree.ElementTree.fromstring(resp.content)
		countryName = root.find("{http://www.worldbank.org}country")[1].text 
		countryObj = Country(code=country,name=countryName)
		countryObj.save()
	return countryObj
	
def getEmbassies(printOut=False):

	embassies = queryAttempts()
	if embassies == None:
		return
	
	# Data that should be update via API need to be deleted first
	Country.objects.filter(autoUpdate=True).delete()
	Embassy.objects.filter(autoUpdate=True).delete()

	for l in ['ways', 'nodes', 'relations']:
		element = getattr(embassies, l)
		for e in element:
			embassy = e.tags
			
			country = embassy['country']
			target = embassy['target']
			
			try:
				countryObjs = canUpdate(country, target) # Checks to see should Embassy should be re-added
			except requests.RequestException:
				print("Unable to map country code to country, skipping Embassy.")
				continue
			if not countryObjs: 
				continue # Embassy is not meant to be updated
			
			name = embassy['name']
			street = embassy['addr:street']
			city = embassy['addr:city']
			phone = embassy['contact:phone']
			data = ", ".join([name,country,target,street,city,phone])
			fax = embassy.get('contact:fax')
			if fax:
				data += ", " + fax
			email = embassy.get('contact:email')
			if email:
				data += ", " + email
			website = embassy.get('contact:website')
			if website:
				data += ", " + website
			
			if printOut:
				print(data.encode("utf-8"))

			govObj, targetObj = countryObjs
			embassyObj = Embassy(government=govObj, location=targetObj, name=name, street_address=street, 
				city=city, phone_number=phone, fax_number=fax, email_address=email, website=website)
			embassyObj.save()
	
	return embassies