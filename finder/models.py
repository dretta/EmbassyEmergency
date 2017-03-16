from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.urls import reverse


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
	elif len(value) != 2:
		raise ValidationError(
			_('%(value)s is not a string size 3'),
			params={'value': value},
		)

def validate_string_all_caps(value):
	if not isinstance(value, str):
		raise ValidationError(
			_('%(value)s is not a string'),
			params={'value': value},
		)
	elif not (value.isupper() and value.isalpha()):
		raise ValidationError(
			_('%(value)s does not have all capital letters'),
			params={'value': value},
		)
		
class AutoUpdateModel(models.Model):
	autoUpdate = models.BooleanField(default=True, db_column="Will Update via Query?")
	start = None
	
	class Meta:
		abstract=True
		

class Country(AutoUpdateModel):

	code = models.CharField(primary_key=True, max_length=2, validators=[validate_nonempty, validate_string_length_three, validate_string_all_caps]) #ISO Alpha-3 Country Code
	name = models.CharField(max_length=50, db_column="Name", validators=[validate_nonempty])
	
	def get_absolute_url(self):
		return reverse('finder:country_info', args=(self.code,))
	
	@receiver(pre_save)
	def pre_save_handler(sender, instance, *args, **kwargs):
		instance.clean()

	def clean(self):
		if self.autoUpdate and self.start != (self.code, self.name):
			self.autoUpdate = False
		
	def __init__(self, *args, **kwargs):
		super(Country, self).__init__(*args, **kwargs)
		self.start = (self.code,self.name)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Country'
		verbose_name_plural = 'Countries'


class Embassy(AutoUpdateModel):
	government = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="government")
	location = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="location")
	name = models.CharField(max_length=200, db_column="Name", validators=[validate_nonempty])
	street_address = models.CharField(max_length=200, db_column="Address")
	city = models.CharField(max_length=50, db_column="City")
	
	phone_number = PhoneNumberField(default=-1, db_column="Phone Number")
	fax_number = PhoneNumberField(null=True, blank=True, db_column="Fax Number")
	
	email_address = models.CharField(null=True, blank=True, max_length=200, db_column="Email")
	website = models.CharField(null=True, blank=True, max_length=200, db_column="Link")
	
	@receiver(pre_save)
	def pre_save_handler(sender, instance, *args, **kwargs):
		instance.clean()
		
	def clean(self):
		if self.government == self.location:
			raise ValidationError(
				_('An embassy cannot have the same government and location.'))
		if self.autoUpdate and self.start != (self.government,self.location,self.name,self.street_address,self.city,self.phone_number,self.fax_number,self.email_address,self.website):
			self.autoUpdate = False
		if not self.autoUpdate:
			self.government.autoUpdate = False
			self.government.save()
			self.location.autoUpdate = False
			self.location.save()

	def __init__(self, *args, **kwargs):
		super(Embassy, self).__init__(*args, **kwargs)
		self.start = (self.government,self.location,self.name,self.street_address,self.city,self.phone_number,self.fax_number,self.email_address,self.website)
			
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Embassy'
		verbose_name_plural = 'Embassies'
		


