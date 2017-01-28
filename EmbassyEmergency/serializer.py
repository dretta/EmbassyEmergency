from rest_framework import serializers
from .models import Country, Embassy

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
		
class EmbassySerializer(serializers.ModelSerializer):
    class Meta:
        model = Embassy