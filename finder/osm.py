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
			""")
	except json.decoder.JSONDecodeError as e: 
		if attempts > 0:
			print("Query failed, {} number of attempt(s) left".format(attempts-1))
			time.sleep(60)
			runQuery(attempts-1)
		else:
			raise e

		
	
	return result
	
def getEmbassies():

	embassies = runQuery(3)

	for l in ['ways', 'nodes', 'relations']:
		element = getattr(embassies, l)
		for e in element:
			embassy = e.tags
			print("{},{},{},{},{},{}".format(embassy['name'].encode("utf-8"),
				embassy['country'].encode("utf-8"),
				embassy['target'].encode("utf-8"),
				embassy['addr:street'].encode("utf-8"),
				embassy['addr:city'].encode("utf-8"),
				embassy['contact:phone'].encode("utf-8")))
	
	return embassies