from django.test import TestCase
from .models import Embassy, Country
from django.core.exceptions import ValidationError

class CountryModelTest(TestCase):

	def test_code_length_three(self):
		"""
		A Country's code must exactly be a size of three
		"""
		c = Country(code="A", name="Anarchy")
		with self.assertRaises(ValidationError) as context:
			c.clean_fields()

		self.assertTrue('%s is not a string size 3' % c.code in str(context.exception))

	def test_nonempty_name(self):
		"""
		A Country's name cannot be empty.
		"""
		c = Country(code="ARY", name="")
		with self.assertRaises(ValidationError) as context:
			c.clean_fields()

		self.assertTrue('This field cannot be blank.' in str(context.exception))

# class EmbassyModelTest(TestCase):
	# def test_different_government_location(self):
		# """
		# The countries used for an embassy's government and location should never be the same.
		# """
		# self.assertIs(Embassy(), False)
