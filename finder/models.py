from django.db import models

class Country(models.Model):
	code = models.CharField(primary_key=True, max_length=3) #ISO Alpha-3 Country Code
	name = models.CharField(max_length=50, db_column="Name")

	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Country'
		verbose_name_plural = 'Countries'


class Embassy(models.Model):
	government = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="government")
	location = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="location")
	name = models.CharField(max_length=200, db_column="Name")
	street_address = models.CharField(max_length=200, db_column="Address")
	city = models.CharField(max_length=50, db_column="City")
	phone_number = models.IntegerField(default=-1, db_column="Phone Number")
	fax_number = models.IntegerField(null=True, blank=True, db_column="Fax Number")
	email_address = models.CharField(max_length=200, db_column="Email")
	website = models.CharField(max_length=200, db_column="Link")

	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Embassy'
		verbose_name_plural = 'Embassies'