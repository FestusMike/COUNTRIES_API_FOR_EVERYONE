from rest_framework import serializers
from .models import Continent, Country, State, LocalGovernment


class LocalGovernmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocalGovernment
        fields = ["name"]


class StateSerializer(serializers.ModelSerializer):
    
    local_governments = LocalGovernmentSerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ["name", "capital", "local_governments"]

    
class CountryOnlySerializer(serializers.ModelSerializer):
    continent = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ["continent", "name", "capital", "currency", "language"]

    def get_continent(self, obj):
        return obj.continent.name


class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)
    continent = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ["continent", "name", "capital", "currency", "language", "states"]

    def get_continent(self, obj):
        return obj.continent.name


class ContinentOnlySerializer(serializers.ModelSerializer):
    countries_count = serializers.SerializerMethodField()

    class Meta:
        model = Continent
        fields = ["name", "countries_count"]

    def get_countries_count(self, obj):
        return obj.countries.count()  


class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Continent
        fields = ["name", "countries"]
