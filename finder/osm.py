import overpy



def getEmbassies(): 
	api = overpy.Overpass()
	# fetch all ways and nodes
	result = api.query("""
		[out:csv("name:en")];relation["admin_level"="2"];(._;>;);out body;
		""")