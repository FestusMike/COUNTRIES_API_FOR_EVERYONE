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
    class Meta:
        model = Country
        fields = ["name", "capital", "currency", "language"]


class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ["name", "capital", "currency", "language", "states"]


class ContinentOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ["name"]


class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Continent
        fields = ["name", "countries"]
