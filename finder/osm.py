import overpy



def getEmbassies(): 
	api = overpy.Overpass()
	# fetch all ways and nodes
	result = api.query("""
		[out:json];(node["amenity"="embassy"];way["amenity"="embassy"];relation["amenity"="embassy"]);out tags;
		""")
		
	return result