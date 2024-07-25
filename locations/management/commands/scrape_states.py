import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from locations.models import State, Country


class Command(BaseCommand):
    help = "Scrape regions and their capitals for states and populate the DB"

    def handle(self, *args, **kwargs):
        url = ""
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
            country = Country.objects.get(name="Venezuela")
        except Country.DoesNotExist:
            self.stdout.write(self.style.ERROR("Country Venezuela does not exist in the database."))
            return  

        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 9:  
                region_name = columns[0].text.strip()
                capital_name = columns[9].text.strip()
                
                if region_name:
                    State.objects.update_or_create(
                        name=region_name,
                        defaults={'capital': capital_name or None, 'country': country}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Added/Updated: {region_name} - {capital_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped row with missing data: {columns}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped row with insufficient columns: {columns}'))

        self.stdout.write(self.style.SUCCESS("Scraping and database population completed successfully."))