from django.test import TestCase
from .models import Embassy, Country
from django.core.exceptions import ValidationError

class CountryModelTest(TestCase):

	# def test_three_capital_letter_code(self):
		# """
		# A Country's code must be three captital letters.
		# """
		# c = Country(code="", name="Anarchy")
		# self.assertNotEqual(c.code, "", "Country code is empty")

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
