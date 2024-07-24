from django.urls import path
from .views import (PlanetEarthListView, ContinentListView, CountryListAndSearchView, CountryListByContinentView, 
                    StateListByCountryView, StateDetailByCountryView, LocalGovernmentListByStateView)


urlpatterns = [
    path('planet-earth', PlanetEarthListView.as_view(), name='all-continents-countries-states-sub-divisions'),
    path('continents', ContinentListView.as_view(), name='list-of-available-continents'),
    path('continents/<str:continent_name>/countries', CountryListByContinentView.as_view(), name='fetching-countries-by-continent'),
    path('countries', CountryListAndSearchView.as_view(), name='fetching-all-countries-available-and-searching-for-a-particular-country'),
    path('countries/<str:country_name>/states', StateListByCountryView.as_view(), name='fetch-all-states-in-a-country'),
    path('countries/<str:country_name>/', StateDetailByCountryView.as_view(), name='search-state-in-a-particular-country'),
    path('countries/<str:country_name>/states/<str:state_name>/local-governments', LocalGovernmentListByStateView.as_view(), name='get-all-local-governments-in-a-state'),
]