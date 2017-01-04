from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_nonempty(value):
	if value == "":
		raise ValidationError(
			_('%(value)s is an empty string'),
			params={'value': value},
		)
		
def validate_string_length_three(value):
	if not isinstance(value, str):
		raise ValidationError(
			_('%(value)s is not a string'),
			params={'value': value},
		)
	elif len(value) != 3:
		raise ValidationError(
			_('%(value)s is not a string size 3'),
			params={'value': value},
		)

class Country(models.Model):

	code = models.CharField(primary_key=True, max_length=3, validators=[validate_nonempty, validate_string_length_three]) #ISO Alpha-3 Country Code
	name = models.CharField(max_length=50, db_column="Name", validators=[validate_nonempty])

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