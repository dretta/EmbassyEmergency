import overpy



def getEmbassies(): 
	api = overpy.Overpass()
	# fetch all ways and nodes
	result = api.query("""
		[out:json];(node["amenity"="embassy"]["country"]["target"];way["amenity"="embassy"]["country"]["target"];relation["amenity"="embassy"]["country"]["target"]);out tags;
		""")
		
	return result