from rest_framework import serializers
from .models import Continent, Country, State, LocalGovernment


class LocalGovernmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocalGovernment
        fields = ["id", "name"]


class StateSerializer(serializers.ModelSerializer):
    local_governments = LocalGovernmentSerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ["id", "name", "capital", "local_governments"]


class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "capital", "currency", "states"]


class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Continent
        fields = ["id", "name", "countries"]
