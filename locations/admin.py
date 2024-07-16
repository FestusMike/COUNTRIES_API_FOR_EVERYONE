from django.contrib import admin
from .models import Continent, Country, State, LocalGovernment


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class CountryAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "continent__name",
    ]  


class StateAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "country__name",
    ]  


class LocalGovernmentAreaAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "state__name",
        "state__country__name",
    ]


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(LocalGovernment, LocalGovernmentAreaAdmin)
