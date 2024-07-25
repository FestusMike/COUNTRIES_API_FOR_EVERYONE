import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from locations.models import Country, Continent 

class Command(BaseCommand):
    """Scrape countries and their details from a URL and populate the DB"""

    help = "Scrape country, capital and languages from a provided URL and populate the database."

    def handle(self, *args, **kwargs):
        url = ""

        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve data from {url}. Status code: {response.status_code}"))
            return

        try:
            continent = Continent.objects.get(name="South America")
        except Continent.DoesNotExist:
            self.stdout.write(self.style.ERROR("South America doesn't exist"))
            return

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table')

        if not table:
            self.stdout.write(self.style.ERROR("Failed to find the table in the HTML content."))
            return

        rows = table.find_all('tr')[1:]

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 5:
                country_name = columns[2].text.strip()
                capital_name = columns[3].text.strip()
                languages = columns[4].text.strip().replace('*','')

                if country_name and capital_name and languages:
                    country = Country.objects.update_or_create(
                        name=country_name,
                        defaults={
                            'capital': capital_name,
                            'language': languages,
                            'continent': continent
                        }
                    )
                    if country:
                        self.stdout.write(self.style.SUCCESS(f'Added: {country_name} - {capital_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated: {country_name} - {capital_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped row with missing data: {columns}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped row with insufficient columns: {columns}'))

        self.stdout.write(self.style.SUCCESS("Scraping and database population completed successfully."))
