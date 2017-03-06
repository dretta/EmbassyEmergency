from django.apps import AppConfig


class FinderConfig(AppConfig):
	name = 'finder'
	init = True
	def ready(self):
		import finder.osm as osm
		if self.init:
			#osm.getEmbassies() #Disabled while in development
			init = False