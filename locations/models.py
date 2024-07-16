from django.db import models
from utils.models import BaseModel
# Create your models here.

class Continent(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Continent Name")

    def __str__(self):
        return self.name

    class Meta:
        abstract = False


class Country(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Country Name or Nation")
    capital = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=100, null=True)
    continent = models.ForeignKey(Continent, related_name='countries', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.capital} - {self.language} - {self.continent.name}"

    class Meta:
        abstract = False
        verbose_name_plural = "Countries"


class State(BaseModel):
    name = models.CharField(max_length=100, verbose_name="State Name or Region")
    capital = models .CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.capital} - {self.country.name} - {self.country.continent.name}"

    class Meta:
        abstract = False


class LocalGovernment(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Name of Local Government")
    state = models.ForeignKey(State, related_name='local_governments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.state.name} state - {self.state.country.name}"

    class Meta:
        abstract = False
