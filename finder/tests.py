from django.test import TestCase
from .models import Embassy, Country
from django.core.exceptions import ValidationError

class BaseTestCase(TestCase):

	def create_country(self, code="CTY", name="A Country"):
		return Country(code=code, name=name)
		
	def create_embassy(self, government, location, name="An Embassy", street_address="An Address", 
		city="A City", phone_number=0, fax_number=1, email_address="An Email", website="A Website"):
		return Embassy(government=government, location=location, name=name, street_address=street_address,
			city=city, phone_number=phone_number, fax_number=fax_number, email_address=email_address, website=website)

	def model_validation(self, object, errorMessage, **kwargs):
		obj = object(**kwargs)
		with self.assertRaises(ValidationError) as context:
			obj.full_clean()

		self.assertTrue(errorMessage in str(context.exception))
	
class CountryModelTest(BaseTestCase):

	def test_code_all_upper_case(self):
		"""
		A Country's code must have all capitial letters
		"""
		code = "LoL"
		self.model_validation(Country, "{0} does not have all capital letters".format(code), code=code)

	def test_code_length_three(self):
		"""
		A Country's code must exactly be a size of three
		"""
		code = "A"
		self.model_validation(Country, "{0} is not a string size 3".format(code), code=code)

	def test_nonempty_name(self):
		"""
		A Country's name cannot be empty
		"""
		name = ""
		self.model_validation(Country, "This field cannot be blank.", name=name)

class EmbassyModelTest(BaseTestCase):

	c1 = BaseTestCase.create_country(BaseTestCase, code="ONE", name="Country 1")
	c2 = BaseTestCase.create_country(BaseTestCase, code="TWO", name="Country 2")

	def test_different_government_location(self):
		"""
		The countries used for an embassy's government and location should never be the same.
		"""
		c = self.create_country()
		self.model_validation(Embassy, "An embassy cannot have the same government and location.", government=c, location=c)

	def test_nonempty_name(self):
		"""
		An Embassy's name cannot be empty
		"""
		self.model_validation(Embassy, "This field cannot be blank.", government=self.c1, location=self.c2, name="")