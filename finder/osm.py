import overpy



def getEmbassies(): 
	api = overpy.Overpass()
	# fetch all ways and nodes
	result = api.query("""
	[out:json];
	(
		( 
			node[amenity=embassy]; - node[amenity=embassy][diplomatic][diplomatic!=embassy]; 
			- node[amenity=embassy][!name][!name:en]; 
			- node[amenity=embassy][!country]; 
			- node[amenity=embassy][!target]; 
			- node[amenity=embassy][!addr:street]; 
			- node[amenity=embassy][!addr:city]; 
			- node[amenity=embassy][!contact:phone];
		);
		( way[amenity=embassy];  
			- way[amenity=embassy][diplomatic][diplomatic!=embassy]; 
			- way[amenity=embassy][!name][!name:en];
			- way[amenity=embassy][!country];
			- way[amenity=embassy][!target];
			- way[amenity=embassy][!addr:street];
			- way[amenity=embassy][!addr:city];
			- way[amenity=embassy][!contact:phone];
		);
		( rel[amenity=embassy];  
			- rel[amenity=embassy][diplomatic][diplomatic!=embassy]; 
			- rel[amenity=embassy][!name][!name:en];
			- rel[amenity=embassy][!country];
			- rel[amenity=embassy][!target];
			- rel[amenity=embassy][!addr:street];
			- rel[amenity=embassy][!addr:city];
			- rel[amenity=embassy][!contact:phone];
		);
	);
	out tags;  
		""")
	
	return result