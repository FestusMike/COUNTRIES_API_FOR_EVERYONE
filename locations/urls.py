from django.urls import path
from .views import ContinentListView, CountryListByContinentView, CountryListView, StateListByCountryView, LocalGovernmentListByStateView


urlpatterns = [
    path('continents', ContinentListView.as_view(), name='continent-list'),
    path('continents/<str:continent_name>/countries', CountryListByContinentView.as_view(), name='country-list-by-continent'),
    path('countries', CountryListView.as_view(), name='country-list'),
    path('countries/<str:country_name>/states', StateListByCountryView.as_view(), name='state-list-by-country'),
    path('countries/<str:country_name>/states/<str:state_name>/local-governments', LocalGovernmentListByStateView.as_view(), name='local-government-list-by-state'),
]