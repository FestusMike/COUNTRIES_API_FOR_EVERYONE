from rest_framework import generics
from rest_framework.response import Response
from .models import Continent, Country, State, LocalGovernment
from .serializers import (ContinentSerializer, ContinentOnlySerializer, CountryOnlySerializer,
                          CountrySerializer, StateSerializer, LocalGovernmentSerializer)
from difflib import get_close_matches


class PlanetEarthListView(generics.ListAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "count": queryset.count(),
            "continents": serializer.data
        }
        return Response(response_data)


class ContinentListView(generics.ListAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentOnlySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "count": queryset.count(),
            "continents": serializer.data
        }
        return Response(response_data)


class CountryListByContinentView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    def get(self, request, continent_name, *args, **kwargs):
        
        continent = Continent.objects.filter(name__iexact=continent_name).first()

        if not continent:
            all_continent_names = Continent.objects.values_list('name', flat=True)
            suggestions = get_close_matches(continent_name, all_continent_names, n=1, cutoff=0.8)
            if suggestions:
                suggestion_message = f"Continent '{continent_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"Continent '{continent_name}' isn't found and no suggestions are available."
            return Response({"error": suggestion_message}, status=404)
        
        countries = Country.objects.filter(continent=continent).order_by('name')
        serializer = self.get_serializer(countries, many=True)
        response_data = {
            "continent": continent.name,
            "count": countries.count(),
            "countries": serializer.data
        }
        return Response(response_data)


class CountryListAndSearchView(generics.GenericAPIView):
    
    def get_serializer_class(self):
        if self.request.GET.get('country'):
            return CountrySerializer
        return CountryOnlySerializer

    def get(self, request, *args, **kwargs):
        country_name = request.GET.get('country', '').strip()
        
        if country_name:
            country = Country.objects.filter(name__iexact=country_name).first()
            
            if not country:
                all_country_names = Country.objects.values_list('name', flat=True)
                suggestions = get_close_matches(country_name, all_country_names, n=1, cutoff=0.8)
                if suggestions:
                    suggestion_message = f"Country '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
                else:
                    suggestion_message = f"Country '{country_name}' isn't found and no suggestions are available."
                return Response({"error": suggestion_message}, status=404)
            
            serializer = self.get_serializer(country)
            response_data = {
                "count": 1,
                "country": serializer.data
            }
            return Response(response_data)
        else:
            countries = Country.objects.all().order_by('name')
            serializer = self.get_serializer(countries, many=True)
            response_data = {
                "count": countries.count(),
                "countries": serializer.data
            }
            return Response(response_data)


class StateListByCountryView(generics.GenericAPIView):
    serializer_class = StateSerializer

    def get(self, request, country_name, *args, **kwargs):
        country_name = country_name.strip()
        country = Country.objects.filter(name__iexact=country_name).first()

        if not country:
            all_country_names = Country.objects.values_list('name', flat=True)
            suggestions = get_close_matches(country_name, all_country_names)
            if suggestions:
                suggestion_message = f"Country '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"Country '{country_name}' isn't found and no suggestions are available."
            return Response({"error": suggestion_message}, status=404)

        states = State.objects.filter(country=country).order_by('name')
        serializer = self.get_serializer(states, many=True)
        response_data = {
            "count": states.count(),
            "states": serializer.data
        }
        return Response(response_data)
    

class StateDetailByCountryView(generics.GenericAPIView):
    serializer_class = StateSerializer

    def get(self, request, country_name, *args, **kwargs):
        country_name = country_name.strip()
        state_name = request.GET.get('state', '').strip()

        if not state_name:
            return Response({"error": "State parameter is missing"}, status=400)

        country = Country.objects.filter(name__iexact=country_name).first()

        if not country:
            all_country_names = Country.objects.values_list('name', flat=True)
            suggestions = get_close_matches(country_name, all_country_names)
            if suggestions:
                suggestion_message = f"Country '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"Country '{country_name}' isn't found and no suggestions are available."
            return Response({
                "error": suggestion_message,
                "suggestions": suggestions if suggestions else []
            }, status=404)

        state = State.objects.filter(name__iexact=state_name, country=country).first()

        if not state:
            all_state_names = State.objects.filter(country=country).values_list('name', flat=True)
            suggestions = get_close_matches(state_name, all_state_names)
            if suggestions:
                suggestion_message = f"State '{state_name}' in '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"State '{state_name}' in '{country_name}' isn't found and no suggestions are available."
            return Response({
                "error": suggestion_message,
                "suggestions": suggestions if suggestions else []
            }, status=404)

        serializer = self.get_serializer(state)
        return Response({
            "count": 1,
            "country": country.name,
            "state": serializer.data
        })


class LocalGovernmentListByStateView(generics.GenericAPIView):
    serializer_class = LocalGovernmentSerializer

    def get(self, request, country_name, state_name, *args, **kwargs):
        country_name = country_name.strip()
        state_name = state_name.strip()

        country = Country.objects.filter(name__iexact=country_name).first()
        
        if not country:
            all_country_names = Country.objects.values_list('name', flat=True)
            suggestions = get_close_matches(country_name, all_country_names)
            
            if suggestions:
                suggestion_message = f"Country '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"Country '{country_name}' isn't found and no suggestions are available."
        
            return Response({
                "error": suggestion_message,
                "suggestions": suggestions if suggestions else []
            }, status=404)

        state = State.objects.filter(name__iexact=state_name, country=country).first()
        if not state:
            all_state_names = State.objects.filter(country=country).values_list('name', flat=True)
            suggestions = get_close_matches(state_name, all_state_names)
            if suggestions:
                suggestion_message = f"State '{state_name}' in '{country_name}' isn't found. Did you mean '{suggestions[0]}'?"
            else:
                suggestion_message = f"State '{state_name}' in '{country_name}' isn't found and no suggestions are available."
            return Response({
                "error": suggestion_message,
                "suggestions": suggestions if suggestions else []
            }, status=404)

        local_governments = LocalGovernment.objects.filter(state=state).order_by('name')
        serializer = self.get_serializer(local_governments, many=True)
        
        return Response({
            "count": local_governments.count(),
            "country": country.name,
            "state": state.name,
            "local_governments": serializer.data
        })