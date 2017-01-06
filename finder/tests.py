from django.test import TestCase
from .models import Embassy, Country
from django.core.exceptions import ValidationError

class BaseTestCase(TestCase):

	def create_country(self, code, name):
		return Country(code=code, name=name)

	def model_validation(self, code, name, errorMessage):
		c = Country(code=code, name=name)
		with self.assertRaises(ValidationError) as context:
			c.clean_fields()

		self.assertTrue(errorMessage in str(context.exception))
	
class CountryModelTest(BaseTestCase):

	def test_code_all_upper_case(self):
		"""
		A Country's code must have all capitial letters
		"""
		self.model_validation("LoL", "Anarchy", "LoL does not have all capital letters")

	def test_code_length_three(self):
		"""
		A Country's code must exactly be a size of three
		"""
		self.model_validation("A", "Anarchy", "A is not a string size 3")

	def test_nonempty_name(self):
		"""
		A Country's name cannot be empty
		"""
		self.model_validation("ARY", "", "This field cannot be blank.")

class EmbassyModelTest(BaseTestCase):
	# def test_different_government_location(self):
		# """
		# The countries used for an embassy's government and location should never be the same.
		# """
		# c = self.create_country("LOL", "ANARCHY STATE")
		# e = Embassy(government=c, location=c, name="A Massive Contradiction", 
			# street_address="The End of the World", city="Hypocrisy Town", 
			# phone_number=1111011110, email_address="trolol@edgelord.net",
			# website="fake.com")
		# self.assertIs(Embassy(), False)

	def test_nonempty_name(self):
		"""
		An Embassy's name cannot be empty
		"""
		c = self.create_country("LOL", "ANARCHY STATE")
		e = Embassy(government=c, location=c, name="", 
			street_address="The End of the World", city="Hypocrisy Town", 
			phone_number=1111011110, email_address="trolol@edgelord.net",
			website="fake.com")
			
		with self.assertRaises(ValidationError) as context:
			e.clean_fields()

		self.assertTrue("This field cannot be blank." in str(context.exception))