import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from locations.models import State, Country, Continent

class Command(BaseCommand):
    help = "Scrape regions and their capitals for Ethiopia and populate the DB"

    def handle(self, *args, **kwargs):
        url = "http://www.statoids.com/uvu.html"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve data from {url}. Status code: {response.status_code}"))
            return

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {'class': 'st'})  
        if not table:
            self.stdout.write(self.style.ERROR("Failed to find the table in the HTML content."))
            return

        rows = table.find_all('tr')[1:]  

        try:
            country = Country.objects.get(name="Vanuatu")
        except Country.DoesNotExist:
            self.stdout.write(self.style.ERROR("Country Australia does not exist in the database."))
            return  

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 7:  
                region_name = columns[0].text.strip()
                capital_name = columns[7].text.strip()
                nothing = '-'

                if region_name and capital_name:
                    State.objects.update_or_create(
                        name=region_name,
                        defaults={'capital': capital_name, 'country': country}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added/Updated: {region_name} - {capital_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped row with missing data: {columns}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped row with insufficient columns: {columns}'))

        self.stdout.write(self.style.SUCCESS("Scraping and database population completed successfully."))
