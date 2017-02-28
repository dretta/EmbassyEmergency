import overpy
import json
import time


def runQuery(attempts): 
	api = overpy.Overpass()
	api.max_retry_count = 3
	# fetch all ways and nodes
	result = None
	try:
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
			""")#except overpy.exception.OverpassTooManyRequests as e:
	except json.decoder.JSONDecodeError as e: 
		if attempts > 0:
			print("Query failed, {} number of attempt(s) left".format(attempts-1))
			time.sleep(60)
			return runQuery(attempts-1)
		else:
			raise e
	
		
	
	return result
	
def getEmbassies():

	embassies = runQuery(3)

	for l in ['ways', 'nodes', 'relations']:
		element = getattr(embassies, l)
		for e in element:
			embassy = e.tags
			name = embassy['name']
			country = embassy['country']
			target = embassy['target']
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
			
			print(data.encode("utf-8"))
	
	return embassies