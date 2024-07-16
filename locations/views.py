from rest_framework import generics
from rest_framework.response import Response
from .models import Continent, Country, State, LocalGovernment
from .serializers import ContinentSerializer, CountrySerializer, StateSerializer, LocalGovernmentSerializer

class ContinentListView(generics.ListAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class CountryListByContinentView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    def get(self, request, continent_name, *args, **kwargs):
        continent = Continent.objects.filter(name__iexact=continent_name).first()
        if not continent:
            return Response({"error": "Continent not found"}, status=404)
        countries = Country.objects.filter(continent=continent).order_by('name')
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)


class CountryListView(generics.ListAPIView):
	queryset = Country.objects.all().order_by('name')
	serializer_class = CountrySerializer


class StateListByCountryView(generics.GenericAPIView):
    serializer_class = StateSerializer

    def get(self, request, country_name, *args, **kwargs):
        country = Country.objects.filter(name__iexact=country_name).first()
        if not country:
            return Response({"error": "Country not found"}, status=404)
        states = State.objects.filter(country=country).order_by('name')
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)


class LocalGovernmentListByStateView(generics.GenericAPIView):
    serializer_class = LocalGovernmentSerializer

    def get(self, request, country_name, state_name, *args, **kwargs):
        country = Country.objects.filter(name__iexact=country_name).first()
        if not country:
            return Response({"error": "Country not found"}, status=404)
        state = State.objects.filter(name__iexact=state_name, country=country).first()
        if not state:
            return Response({"error": "State not found"}, status=404)
        local_governments = LocalGovernment.objects.filter(state=state).order_by('name')
        serializer = self.get_serializer(local_governments, many=True)
        return Response(serializer.data)