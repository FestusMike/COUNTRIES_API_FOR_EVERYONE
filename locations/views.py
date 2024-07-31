from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import generics
from rest_framework.response import Response
from .models import Continent, Country, State, LocalGovernment
from .serializers import (ContinentSerializer, ContinentOnlySerializer, CountryOnlySerializer,
                          CountrySerializer, StateSerializer, LocalGovernmentSerializer)
from difflib import get_close_matches


@extend_schema(
    description="Retrieve a list of all continents with detailed information.",
    responses={
        200: ContinentSerializer(many=True),
    },
    )
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


@extend_schema(
    description="Retrieve a list of all continents with basic information.",
    responses={
        200: ContinentOnlySerializer(many=True),
    },
    )
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


@extend_schema(
    description="This endpoint allows for filtering of countries based on their continent. The continent is a compulsory URL parameter.",
    responses={
        200: CountrySerializer(many=True),
        404: OpenApiExample(
            "Error",
            value={
                "error": "Continent 'europe' isn't found. Did you mean 'Europe'?"
            }
        )
    },
    examples=[
        OpenApiExample(
            "Success",
            description="Successful response",
            value={
                "continent": "Europe",
                "count": 3,
                "countries": [
                    {
                        "name": "France",
                        "capital": "Paris",
                        "currency": "Euro",
                        "language": "French"
                    },
                    {
                        "name": "Germany",
                        "capital": "Berlin",
                        "currency": "Euro",
                        "language": "German"
                    },
                    {
                        "name": "Spain",
                        "capital": "Madrid",
                        "currency": "Euro",
                        "language": "Spanish"
                    }
                ]
            }
        ),
        OpenApiExample(
            "Error",
            description="Error response with suggestion",
            value={
                "error": "Continent 'europe' isn't found. Did you mean 'Europe'?"
            }
        )
    ]
)
class CountryListByContinentView(generics.GenericAPIView):
    serializer_class = CountrySerializer

    def get(self, request, continent_name, *args, **kwargs):
        continent_name = continent_name.strip()
        continent = Continent.objects.filter(name__exact=continent_name).first()

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


@extend_schema(
    description="This endpoint allows for listing of all the countries in the database and also a search for a particular country. The search for a particular country involves appending the 'country' key as a query parameter and the name of the country as the value.",
    responses={
        200: OpenApiExample(
            "Success",
            value={
                "count": 1,
                "country": {
                    "name": "France",
                    "capital": "Paris",
                    "currency": "Euro",
                    "language": "French",
                    "states": []
                }
            }
        ),
        404: OpenApiExample(
            "Error",
            value={
                "error": "Country 'france' isn't found. Did you mean 'France'?"
            }
        )
    },
    parameters=[
         OpenApiParameter(name='country', description='Name of the country to search for', required=False, type=str)
    ],
    examples=[
        OpenApiExample(
            "No Query Parameter",
            description="Successful response without a query parameter",
            value={
                "count": 3,
                "countries": [
                    {
                        "name": "France",
                        "capital": "Paris",
                        "currency": "Euro",
                        "language": "French"
                    },
                    {
                        "name": "Germany",
                        "capital": "Berlin",
                        "currency": "Euro",
                        "language": "German"
                    },
                    {
                        "name": "Spain",
                        "capital": "Madrid",
                        "currency": "Euro",
                        "language": "Spanish"
                    }
                ]
            }
        )
    ]
)
class CountryListAndSearchView(generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.GET.get('country'):
            return CountrySerializer
        return CountryOnlySerializer

    def get(self, request, *args, **kwargs):
        country_name = request.GET.get('country', '').strip()

        if country_name:
            country = Country.objects.filter(name__exact=country_name).first()

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


@extend_schema(
    description= " This endpoint allows for fetching all states based on their country. The country name must be appended to the URL as a parameter",
    responses={
        200: OpenApiExample(
            "Success",
            value={
                "count": 2,
                "states": [
                    {
                        "name": "Ile-de-France",
                        "capital": "Paris"
                    },
                    {
                        "name": "Occitanie",
                        "capital": "Toulouse"
                    }
                ]
            }
        ),
        404: OpenApiExample(
            "Error",
            value={
                "error": "Country 'france' isn't found. Did you mean 'France'?"
            }
        )
    },
    examples=[
        OpenApiExample(
            "No States Found",
            description="No states found for the given country",
            value={
                "count": 0,
                "states": []
            }
        )
    ]
)
class StateListByCountryView(generics.GenericAPIView):
    serializer_class = StateSerializer

    def get(self, request, country_name, *args, **kwargs):
        country_name = country_name.strip()
        country = Country.objects.filter(name__exact=country_name).first()

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
    

@extend_schema(
    description="This endpoint allows for fetching details of a particular state in a country. The 'state' key is appended to the url as a compulsory query parameter and the state name is the value",
    responses={
        200: OpenApiExample(
            "Success",
            value={
                "count": 1,
                "country": "France",
                "state": {
                    "name": "Ile-de-France",
                    "capital": "Paris"
                }
            }
        ),
        404: OpenApiExample(
            "Error - Country Not Found",
            value={
                "error": "Country 'france' isn't found. Did you mean 'France'?",
                "suggestions": ["France"]
            }
        ),
        404: OpenApiExample(
            "Error - State Not Found",
            value={
                "error": "State 'ile-de-france' in 'France' isn't found. Did you mean 'Ile-de-France'?",
                "suggestions": ["Ile-de-France"]
            }
        ),
        400: OpenApiExample(
            "Error - Missing State Parameter",
            value={
                "error": "State parameter is missing"
            }
        )
    },
    parameters=[
        OpenApiParameter(name='state', description='Name of the state to search', required=True, type=str)
     ],
    examples=[
        OpenApiExample(
            "Success Response",
            description="Successful response with the state details",
            value={
                "count": 1,
                "country": "France",
                "state": {
                    "name": "Ile-de-France",
                    "capital": "Paris"
                }
            }
        )
    ]
)
class StateDetailByCountryView(generics.GenericAPIView):
    serializer_class = StateSerializer

    def get(self, request, country_name, *args, **kwargs):
        country_name = country_name.strip()
        state_name = request.GET.get('state', '').strip()

        if not state_name:
            return Response({"error": "State parameter is missing"}, status=400)

        country = Country.objects.filter(name__exact=country_name).first()

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


@extend_schema(
    description="This endpoint allows for fetching all the local governments in a particular state. Here, the country name and state name are appended to the url as parameters",
    responses={
        200: OpenApiExample(
            "Success",
            value={
                "count": 2,
                "country": "Nigeria",
                "state": "Lagos",
                "local_governments": [
                    {"name": "Ikeja"},
                    {"name": "Surulere"}
                ]
            }
        ),
        404: OpenApiExample(
            "Error - Country Not Found",
            value={
                "error": "Country 'nigeria' isn't found. Did you mean 'Nigeria'?",
                "suggestions": ["Nigeria"]
            }
        ),
        404: OpenApiExample(
            "Error - State Not Found",
            value={
                "error": "State 'lagos' in 'Nigeria' isn't found. Did you mean 'Lagos'?",
                "suggestions": ["Lagos"]
            }
        ),
    },
    examples=[
        OpenApiExample(
            "Success Response",
            description="Successful response with the list of local governments in the state",
            value={
                "count": 2,
                "country": "Nigeria",
                "state": "Lagos",
                "local_governments": [
                    {"name": "Ikeja"},
                    {"name": "Surulere"}
                ]
            }
        )
    ]
)
class LocalGovernmentListByStateView(generics.GenericAPIView):
    serializer_class = LocalGovernmentSerializer

    def get(self, request, country_name, state_name, *args, **kwargs):
        country_name = country_name.strip()
        state_name = state_name.strip()

        country = Country.objects.filter(name__exact=country_name).first()
        
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

        state = State.objects.filter(name__exact=state_name, country=country).first()
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