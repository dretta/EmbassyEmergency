import overpy



def getEmbassies(): 
	api = overpy.Overpass()
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
	
	for l in ['ways', 'nodes', 'relations']:
		element = getattr(result, l)
		for e in element:
			embassy = e.tags
			print("{},{},{},{},{},{}".format(embassy['name'].encode("utf-8"),
				embassy['country'].encode("utf-8"),
				embassy['target'].encode("utf-8"),
				embassy['addr:street'].encode("utf-8"),
				embassy['addr:city'].encode("utf-8"),
				embassy['contact:phone'].encode("utf-8")))
	
	return result